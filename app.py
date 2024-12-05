from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import Config
import requests
import json
import os

# Inicializar a aplicação
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# Modelo de Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, senha):
        from werkzeug.security import generate_password_hash
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.senha_hash, senha)

# Modelo de Rota
class Rota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    criador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ponto_partida = db.Column(db.String(255), nullable=False)
    destino_principal = db.Column(db.String(255), nullable=False)
    waypoints = db.Column(db.Text)
    criador = db.relationship('User', backref=db.backref('rotas', lazy=True))

class PontoTuristico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rota_id = db.Column(db.Integer, db.ForeignKey('rota.id'), nullable=False)
    rota = db.relationship('Rota', backref=db.backref('pontos_turisticos', lazy=True))

# Página inicial
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main'))
    return redirect(url_for('login'))

# Tela de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(senha):
            session['user_id'] = user.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main'))
        else:
            flash('E-mail ou senha inválidos.', 'danger')

    return render_template('login.html')

# Tela de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está em uso.', 'danger')
            return redirect(url_for('cadastro'))

        novo_usuario = User(nome=nome, email=email)
        novo_usuario.set_password(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Página principal
@app.route('/main')
def main():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar a página principal.', 'danger')
        return redirect(url_for('login'))
    
    # Buscar as 3 rotas mais recentes
    trending_rotas = Rota.query.order_by(Rota.criado_em.desc()).limit(2).all()

    return render_template('main.html', trending_rotas=trending_rotas)

# Gerar rota
@app.route('/gerar-rota', methods=['GET', 'POST'])
def gerar_rota():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar esta funcionalidade.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        ponto_partida = request.form.get('ponto_partida')
        destino_principal = request.form.get('destino_principal')

        if not ponto_partida or not destino_principal:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('gerar_rota'))

        return redirect(url_for('buscar_pontos_turisticos', ponto_partida=ponto_partida, destino_principal=destino_principal))

    return render_template('gerar_rota.html')

# Buscar pontos turísticos
@app.route('/buscar-pontos-turisticos', methods=['POST'])
def buscar_pontos_turisticos():
    if not request.is_json:
        return jsonify({"error": "Requisição deve conter JSON válido."}), 400

    data = request.get_json()
    ponto_partida = data.get('ponto_partida', '').strip()
    destino = data.get('destino_principal', '').strip()
    interesses = data.get('interesses', [])  # Lista de interesses turísticos

    if not ponto_partida or not destino:
        return jsonify({"error": "Os campos 'ponto_partida' e 'destino_principal' são obrigatórios."}), 400

    try:
        google_api_key = app.config['GOOGLE_MAPS_API_KEY']
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        directions_url = "https://maps.googleapis.com/maps/api/directions/json"

        # Obter coordenadas do ponto de partida
        geocode_response = requests.get(
            f"https://maps.googleapis.com/maps/api/geocode/json?address={ponto_partida}&key={google_api_key}"
        )
        geocode_data = geocode_response.json()
        if geocode_data['status'] != "OK":
            return jsonify({"error": "Ponto de partida inválido."}), 400
        origem_coords = geocode_data['results'][0]['geometry']['location']

        # Buscar pontos turísticos ao longo da rota
        directions_response = requests.get(directions_url, params={
            "origin": ponto_partida,
            "destination": destino,
            "key": google_api_key
        })
        directions_data = directions_response.json()
        if directions_data.get('status') != "OK":
            return jsonify({"error": "Não foi possível gerar a rota."}), 500

        steps = directions_data['routes'][0]['legs'][0]['steps']
        waypoints = [{"lat": step['start_location']['lat'], "lng": step['start_location']['lng']} for step in steps]

        # Filtrar pontos turísticos para cada etapa da rota
        pontos_turisticos = []
        for step in steps:
            location = step['end_location']
            for interesse in interesses:
                response = requests.get(places_url, params={
                    "location": f"{location['lat']},{location['lng']}",
                    "radius": 1000,  # Busca em um raio de 1km
                    "type": interesse,
                    "key": google_api_key
                })
                places_data = response.json()
                if places_data.get('results'):
                    for place in places_data['results']:
                        pontos_turisticos.append({
                            "nome": place['name'],
                            "latitude": place['geometry']['location']['lat'],
                            "longitude": place['geometry']['location']['lng'],
                            "tipo": interesse
                        })

        # Criar a rota no banco de dados
        user_id = session.get('user_id')
        nova_rota = Rota(
            descricao=f"Rota de {ponto_partida} para {destino}.",
            criador_id=user_id,
            ponto_partida=ponto_partida,
            destino_principal=destino,
            waypoints=json.dumps(waypoints)
        )
        db.session.add(nova_rota)
        db.session.commit()

        # Adicionar pontos turísticos ao banco de dados
        for ponto in pontos_turisticos:
            novo_ponto = PontoTuristico(
                nome=ponto['nome'],
                descricao=ponto.get('tipo', ''),
                latitude=ponto['latitude'],
                longitude=ponto['longitude'],
                rota_id=nova_rota.id
            )
            db.session.add(novo_ponto)

        db.session.commit()

        return jsonify({"rota_id": nova_rota.id}), 200

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# Obter detalhes da rota em JSON
@app.route('/get_route/<int:rota_id>')
def get_route(rota_id):
    rota = Rota.query.get_or_404(rota_id)
    pontos_turisticos = [
        {
            "nome": ponto.nome,
            "descricao": ponto.descricao,
            "lat": ponto.latitude,
            "lng": ponto.longitude
        } for ponto in rota.pontos_turisticos
    ]
    return jsonify({
        "origin": rota.ponto_partida,
        "destination": rota.destino_principal,
        "tourist_points": pontos_turisticos
    })

# Visualizar rota
@app.route('/rota/<int:rota_id>')
def visualizar_rota(rota_id):
    rota = Rota.query.get_or_404(rota_id)

    # Carrega os waypoints
    waypoints = json.loads(rota.waypoints) if rota.waypoints else []

    # Passa a API Key dinamicamente para o template
    google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    return render_template(
        'rota.html',
        ponto_partida=rota.ponto_partida,
        destino_principal=rota.destino_principal,
        waypoints=json.dumps(waypoints),
        google_api_key=google_api_key  # Incluído
    )

# Perfil
@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar o perfil.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    limit = 5  # Número máximo de rotas por solicitação
    offset = int(request.args.get('offset', 0))

    # Consulta para obter as rotas com limite e offset
    minhas_rotas = Rota.query.filter_by(criador_id=user_id).order_by(Rota.criado_em.desc()).limit(limit).offset(offset).all()
    
    if request.args.get('json'):
        rotas_json = [
            {
                "id": rota.id,
                "descricao": rota.descricao,
                "criado_em": rota.criado_em.strftime('%d/%m/%Y'),
            } for rota in minhas_rotas
        ]
        return jsonify(rotas_json)

    # Rotas iniciais para a página
    return render_template('profile.html', minhas_rotas=minhas_rotas, limit=limit)

# Dúvidas
@app.route('/duvidas')
def duvidas():
    return render_template('duvidas.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
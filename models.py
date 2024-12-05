from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

class Rota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    criador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ponto_partida = db.Column(db.String(255), nullable=False)
    destino_principal = db.Column(db.String(255), nullable=False)
    criador = db.relationship('User', backref=db.backref('rotas', lazy=True))

class PontoTuristico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rota_id = db.Column(db.Integer, db.ForeignKey('rota.id'), nullable=False)
    rota = db.relationship('Rota', backref=db.backref('pontos_turisticos', lazy=True))

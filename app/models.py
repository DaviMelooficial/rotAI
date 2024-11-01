from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class TouristPoint(db.Model):
    __tablename__ = 'tourist_points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    estimated_cost = db.Column(db.Float, nullable=False)

class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Text, nullable=False)  # Armazena IDs ou detalhes dos pontos turísticos como JSON
    total_cost = db.Column(db.Float, nullable=False)

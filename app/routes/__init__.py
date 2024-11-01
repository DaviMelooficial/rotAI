from flask import Blueprint
from .user_routes import user_bp
from .route_routes import route_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(route_bp)

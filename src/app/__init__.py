from flask import Flask
from app.database import db
from app.api.v1.clients import client_bp  
from app.api.v1.supplier import supplier_bp
from app.api.v1.product import product_bp
from app.api.v1.images import image_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1415@db:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(client_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(image_bp)

    return app

import os
from flask import Flask
from dotenv import load_dotenv
from main.routes import main

def create_app():
    # Inicializo la aplicacion
    app = Flask(__name__,static_folder='main/static')

    # Cargo las variables de entorno
    load_dotenv()

    # Configuro las variables de entorno
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config["API_URL"] = os.getenv("API_URL")

    # Registro los blueprints
    app.register_blueprint(main.app)

    return app 
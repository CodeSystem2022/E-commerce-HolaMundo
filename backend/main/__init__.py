import os
from flask import Flask
from dotenv import load_dotenv
# Import RESTful
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


# Instanciando la api
api = Api()

# Instanciando la base de datos
db = SQLAlchemy()

#INicializador jwt
jwt = JWTManager()

def create_app():
    # Instanciando la aplicación
    app = Flask(__name__)

    # Cargando variables de entorno
    load_dotenv()

    # SI no existe base de datos, crearlo
    if not os.path.exists(os.getenv("DB_PATH")+os.getenv("DB_NAME")):
        os.mknod(os.getenv("DB_PATH")+os.getenv("DB_NAME"))
    
    # Configuración de la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de la URL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv("DB_PATH")+os.getenv("DB_NAME")

    # Inicializador de la base de datos
    db.init_app(app)

    # Importamos los controladores
    import main.controllers as controllers

    # Api load resource
    api.add_resource(controllers.OrderResource, '/order/<int:id>')
    api.add_resource(controllers.OrdersResource, '/orders')

    api.add_resource(controllers.ProductResource, '/product/<int:id>')
    api.add_resource(controllers.ProductsResource, '/products')

    api.add_resource(controllers.FoodResource, '/food/<int:id>')
    api.add_resource(controllers.FoodsResource, '/foods')

    api.add_resource(controllers.UserResource, '/user/<int:id>')
    api.add_resource(controllers.UsersResource, '/users')

    api.add_resource(controllers.ImageResource, '/image/<int:id>')

    # Inicializador Api
    api.init_app(app)

    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))

    # Inicializador JWT
    jwt.init_app(app)

    from main.auth import routes
    app.register_blueprint(auth.routes.auth)


    return app
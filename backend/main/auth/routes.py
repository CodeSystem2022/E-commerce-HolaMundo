from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from main.services import UserService
from main.map import UserSchema

# Instanciando el blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')
service = UserService()
schema = UserSchema()

#login 
@auth.route('/login', methods=['POST'])
def login():

    user = service.get_by_email(request.json.get('email'))
    if user:
        if user.password == request.json.get('password'):
            #Creacion del token
            access_token = create_access_token(identity=user)
            data = {
                'id': user.id,
                'email': user.email,
                'access_token': access_token,
            }
            return data, 200
        else:
            return {'message': 'Password incorrect'}, 401
    else:
        return {'message': 'User not found'}, 404
    
@auth.route('/register', methods=['POST'])
def register():
    user = schema.load(request.json)
    exist = service.get_by_email(user.email)
    if exist:
        return {'message': 'User already exists'}, 409
    else:
        try:
            user = service.add(user)
            return schema.dump(user), 201
        except:
            return {'message': 'Error creating user'}, 500
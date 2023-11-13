from flask_restful import Resource
from main.models import UserModel
from flask import request
from .. import db
from main.map import UserSchema
from flask import jsonify
from main.services import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators

class User(Resource):

    def __init__(self):
        self.__schema = UserSchema()
        self.__service = UserService() 

    @jwt_required()
    def get(self, id):
        # Verify identity
        current_user = get_jwt_identity()
        if current_user:
            user_data = self.__schema.dump(self.__service.get_by_id(id)), 201
            return user_data
        else:
            return {'message': 'Not allowed'}, 403
    
    @jwt_required()
    def put(self, id):
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id)
        claims = get_jwt()
        if claims['role'] == 'admin' or current_user_id == id:
            user = self.__service.get_by_id(id)
            if user:
                data = request.get_json().items()
                for key, value in data:
                    setattr(user, key, value)
                user_data = self.__schema.dump(self.__service.update(user)), 201
                return jsonify(user_data)
            return {'message': 'User not found'}, 404
        else:
            return {'message': 'Not allowed'}, 403
    
    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id)
        claims = get_jwt()
        #current_
        if claims['role'] == 'admin' or current_user_id == id:
            user = self.__service.get_by_id(id)
            if user:
                self.__service.delete(id)
                return {'message': 'User deleted successfully'}, 200
            return {'message': 'User not found'}, 404
        else:
            return {'message': 'Not allowed'}, 403

    

class Users(Resource):

    def __init__(self):
        self.__schema = UserSchema() 
        self.__service = UserService()

    @admin_required
    def get(self):
        user_data = self.__schema.dump(self.__service.get_all(), many=True)
        return user_data
    
    @admin_required
    def post(self):
        user = self.__schema.load(request.get_json())
        user_data = self.__schema.dump(self.__service.add(user))
        return user_data
from flask_restful import Resource
from main.models import ProductModel
from flask import request
from .. import db
from main.map import FoodSchema
from flask import jsonify
from main.services import FoodService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators

class Food(Resource):

    def __init__(self):
        self.__schema = FoodSchema()
        self.__Service = FoodService()

    @jwt_required(optional=True)
    def get(self, id):
        food_Data = self.__schema.dump(self.__Service.get_by_id(id)), 201
        return food_Data
    
    @admin_required
    def put(self, id):
        food = self.__service.get_by_id(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(food, key ,value)
        food_data = self.__schema.dump(self.__service.update(product)), 201
        return jsonify(food_data)
    
    @admin_required
    def delete(self, id):
        food = self.__service.get_by_id(id)
        if food:
            self.__service.delete(id)
            return {'message': 'Product deleted'}, 200
        return {'message': 'Product not found'}, 404
    
class Foods(Resource):

    def __init__(self):
        self.__schema = FoodSchema()
        self.__service = FoodService()

    @jwt_required(optional=True)
    def get(self):
        foods = self.__service.get_all()
        food_data = self.__schema.dump(foods, many=True)
        return food_data

    @admin_required
    def post(self):
        food = self.__schema.load(request.get_json())
        food_data = self.__schema.dump(self.__service.add(food))
        return food_data
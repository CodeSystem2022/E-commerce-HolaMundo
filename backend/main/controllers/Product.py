from flask_restful import Resource
from main.models import ProductModel
from flask import request
from .. import db
from main.map import ProductSchema
from flask import jsonify
from main.services import ProductService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators

class Product(Resource):

    def __init__(self):
        self.__schema = ProductSchema()
        self.__Service = ProductService()

    @jwt_required(optional=True)
    def get(self, id):
        product_Data = self.__schema.dump(self.__Service.get_by_id(id)), 201
        return product_Data
    
    @admin_required
    def put(self, id):
        product = self.__service.get_by_id(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(product, key ,value)
        product_data = self.__schema.dump(self.__service.update(product)), 201
        return jsonify(product_data)
    
    @admin_required
    def delete(self, id):
        product = self.__service.get_by_id(id)
        if product:
            self.__service.delete(id)
            return {'message': 'Product deleted'}, 200
        return {'message': 'Product not found'}, 404
    
class Products(Resource):

    def __init__(self):
        self.__schema = ProductSchema()
        self.__service = ProductService()

    @jwt_required(optional=True)
    def get(self):
        products = self.__service.get_all()
        product_data = self.__schema.dump(products, many=True)
        return product_data

    @jwt_required()
    def post(self):
        product = self.__schema.load(request.get_json())
        product_data = self.__schema.dump(self.__service.add(product))
        return product_data
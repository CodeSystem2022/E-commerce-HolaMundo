from flask_restful import Resource
from main.models import OrderModel
from flask import request
from .. import db
from main.map import OrderSchema
from flask import jsonify
from main.services import OrderService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators

class Order(Resource):

    def __init__(self):
        self.__schema = OrderSchema()
        self.__service = OrderService()

    @jwt_required()
    def get(self, id):
        order_data = self.__schema.dump(self.__service.get_by_id(id)), 201
        # Verify identity
        current_user = get_jwt_identity()
        if current_user:
            return order_data
        else:
            return {'message': 'Not allowed'}, 403

    @jwt_required()
    def put(self, id):
        order = self.__service.get_by_id(id)
        current_user = get_jwt_identity()
        if current_user:
            if order:
                data = request.get_json().items()
                for key, value in data:
                    setattr(order, key, value)
                order_data = self.__schema.dump(self.__service.update(order)), 201
                return jsonify(order_data)
            return {'message': 'Order not found'}, 404
        else:
            return {'message': 'Not allowed'}, 403
        
    @jwt_required()
    def delete(self, id):
        order = self.__service.get_by_id(id)
        current_user = get_jwt_identity()
        if current_user:
            if order:
                self.__service.delete(id)
                return {'message': 'Order deleted successfully'}, 200
            return {'message': 'Order not found'}, 404
        else:
            return {'message': 'Not allowed'}, 403

    
class Orders(Resource):

    def __init__(self):
        self.__schema = OrderSchema()
        self.__service = OrderService()

    @admin_required
    def get(self):
        order_data = self.__schema.dump(self.__service.get_all(), many=True)
        return order_data

    @jwt_required()
    def post(self):
        order = self.__schema.load(request.get_json())
        current_user = get_jwt_identity()
        if current_user:
            order_data = self.__schema.dump(self.__service.add(order))
            return order_data, 201
        else:
            return {'message': 'Not allowed'}, 403

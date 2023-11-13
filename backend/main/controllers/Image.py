from flask_restful import Resource
from main.models import ImageModel
from flask import request
from .. import db
from main.map import ImageSchema
from flask import jsonify
from main.services import ImageService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.auth import decorators

class Image(Resource):

    def __init__(self):
        self.__schema = ImageSchema()
        self.__service = ImageService()

    @jwt_required()
    def get(self, id):
        image_data = self.__schema.dump(self.__service.get_by_id(id)), 201
        # Verify identity
        current_user = get_jwt_identity()
        if current_user:
            return image_data
        else:
            return {'message': 'Not allowed'}, 403
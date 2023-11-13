from marshmallow import Schema, fields, validate, post_load
from main.models import UserModel

class UserSchema(Schema):
    '''
    User schema para serializar y deserializar objetos User
    '''
    id = fields.Integer()
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, validate=validate.Length(min=3, max=120))
    password = fields.String(required=True, validate=validate.Length(min=3, max=80))
    phone = fields.Integer(required=True)
    role = fields.String(required=True, validate=validate.Length(min=3, max=10))
    address = fields.String(required=True, validate=validate.Length(min=3, max=120))

    @post_load
    def make_user(self, data, **kwargs):
        '''
        Crea objeto tipo Usermodel a partir de un diccionario
        '''
        return UserModel(**data)
    
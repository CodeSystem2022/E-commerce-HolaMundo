from marshmallow import Schema, fields, validate, post_load
from main.models import FoodModel

class FoodSchema(Schema):
    '''
    Food schema para serializar y deserializar objetos food
    '''
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=3, max=50))
    description = fields.String(required=True, validate=validate.Length(min=3, max=120))
    price = fields.Float(required=True)
    category = fields.String(required=True, validate=validate.Length(min=3, max=120))
    image_id = fields.Integer(required=False)

    @post_load
    def make_food(self, data, **kwargs):
        '''
        Crea objeto tipo Productmodel a partir de un diccionario
        '''
        return FoodModel(**data)
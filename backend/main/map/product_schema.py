from marshmallow import Schema, fields, validate, post_load
from main.models import ProductModel

class ProductSchema(Schema):
    '''
    Product schema para serializar y deserializar objetos Product
    '''
    id = fields.Integer()
    order_id = fields.Integer(required=True)
    food_id = fields.Integer(required=True)
    
    @post_load
    def make_product(self, data, **kwargs):
        '''
        Crea objeto tipo ProductModel a partir de un diccionario
        '''
        return ProductModel(**data)
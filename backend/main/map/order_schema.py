from marshmallow import Schema, fields, validate, post_load
from main.models import OrderModel

class OrderSchema(Schema):
    '''
    Order schema para serializar y deserializar objetos Order
    '''
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    status = fields.String(required=True, validate=validate.Length(min=3, max=120))
    description = fields.String(required=True, validate=validate.Length(min=3, max=120))
    date = fields.DateTime(required=True)
    
    
    products = fields.List(fields.Nested('ProductSchema'))

    @post_load
    def make_order(self, data, **kwargs):
        '''
        Crea objeto tipo Ordermodel a partir de un diccionario
        '''
        return OrderModel(**data)

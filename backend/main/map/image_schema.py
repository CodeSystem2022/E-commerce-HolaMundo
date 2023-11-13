from marshmallow import Schema, fields, validate, post_load
from main.models import ImageModel

class ImageSchema(Schema):
    '''
    Image schema para serializar y deserializar objetos Image
    '''
    id = fields.Integer()

    @post_load
    def make_image(self, data, **kwargs):
        '''
        Crea objeto tipo Imagemodel a partir de un diccionario
        '''
        return ImageModel(**data)
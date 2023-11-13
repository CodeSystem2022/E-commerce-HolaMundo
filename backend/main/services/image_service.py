from main.services.service import Service
from main.repositories import ImageRepository

class ImageService(Service):
    '''
    Herencia de métodos de service.py para la entidad Image
    '''
    
    def __init__(self):
        self.__repository = ImageRepository()

    @property
    def repository(self):
        return self.__repository
    
    def get_by_id(self, id):
        return self.__repository.find_by_id(id)
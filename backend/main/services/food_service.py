from main.services.service import Service
from main.repositories import FoodRepository 

class FoodService(Service):
    '''
    Herencia de métodos de service.py para la entidad Product
    '''

    def __init__(self):
        self.__repository = FoodRepository()

    @property
    def repository(self):
        return self.__repository

    def add(self, model):
        return self.__repository.create(model)

    def get_all(self):
        return self.__repository.find_all()

    def get_by_id(self, id):
        return self.__repository.find_by_id(id)
    
    def get_by_email(self, email):
        pass
    
    def update(self, model):
        return self.__repository.update(model)

    def delete(self, id):
        return self.__repository.delete(id)
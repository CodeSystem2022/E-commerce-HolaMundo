from abc import ABC, abstractmethod

class Service(ABC):

    '''
    CLase abstracta que define los métodos que deben implementar las clases que hereden de ella
    '''
    @abstractmethod
    def add(self, model):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def update(self, model):
        pass

    @abstractmethod
    def delete(self, id):
        pass

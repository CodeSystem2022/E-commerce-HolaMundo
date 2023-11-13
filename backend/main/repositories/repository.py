from abc import ABC, abstractmethod
from .. import db

class Create(ABC):

    @abstractmethod
    def create(self,model:db.Model):
        ''''
        Metodo abstracto que crea un registro en la base de datos
        '''
        pass


class Read(ABC):

    @abstractmethod
    def find_all(self):
        ''''
        Metodo abstracto que retorna todos los registros de una tabla
        '''
        pass

    @abstractmethod
    def find_by_id(self,id: int) -> db.Model:
        ''''
        Metodo abstracto que retorna un registro de una tabla
        '''
        pass

    @abstractmethod
    def find_by_email(self,email: str) -> db.Model:
        ''''
        Metodo abstracto que retorna un registro de una tabla
        '''
        pass


class Update(ABC):
    
        @abstractmethod
        def update(self,model:db.Model):
            ''''
            Metodo abstracto que actualiza un registro en la base de datos
            '''
            pass


class Delete(ABC):
         
        @abstractmethod
        def delete(self,id: int):
            ''''
            Metodo abstracto que elimina un registro en la base de datos
            '''
            pass
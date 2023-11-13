from main.repositories.repository import Create, Read, Update, Delete
from main.models import UserModel
from .. import db

#IMplementación de los métodos abstractos de la clase abstracta Repository heredando el CRUD
class UserRepository(Create, Read, Update, Delete):
    def __init__(self):
        self.__type_model = UserModel

    #getter
    @property
    def type_model(self):
        return self.__type_model
    
    def create(self, model: db.Model):

        # password_hashed = self.__type_model.generate_password(model.password)

        # model = UserModel(
        #     username=model.username,
        #     email=model.email,
        #     password=password_hashed,
        #     phone=model.phone,
        #     role=model.role,
        #     address=model.address 
        # )
        db.session.add(model)
        db.session.commit()
        return model
    
    def find_all(self):
        model = db.session.query(self.__type_model).all()
        return model
    
    def find_by_id(self,id: int) -> db.Model:
        model = db.session.query(self.__type_model).filter_by(id=id).first()
        return model
    
    def find_by_email(self, email: str) -> db.Model:
        model = db.session.query(self.__type_model).filter_by(email=email).first()
        return model
    
    def update(self,model: db.Model):
        db.session.add(model)
        db.session.commit()
        return model
    
    def delete(self,id: int):
        model = db.session.query(self.__type_model).filter_by(id=id).first()
        db.session.delete(model)
        db.session.commit()
        return model
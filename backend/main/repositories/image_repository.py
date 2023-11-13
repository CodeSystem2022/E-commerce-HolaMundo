from main.repositories.repository import Read
from main.models import ImageModel
from .. import db


class ImageRepository(Read):
    def __init__(self):
        self.__type_model = ImageModel

    # getter
    @property
    def type_model(self):
        return self.__type_model

    def find_by_id(self, id: int) -> db.Model:
        model = db.session.query(self.__type_model).filter_by(id=id).first()
        return model
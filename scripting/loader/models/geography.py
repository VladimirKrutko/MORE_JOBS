from scripting.loader.base_model import *


class Geography(Base, BaseModel):
    """
    Модель для таблицы 'geography'.
    Наследуется от BaseModel, включает базовые методы и поля.
    """
    __tablename__ = "geography"

    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    def __repr__(self):
        return f"<Geography(id={self.id}, city='{self.city}', country='{self.country}')>"

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from MORE_JOBS.scripting.loader.base_model import BaseModel
from MORE_JOBS.scripting.loader.db_setup import Base, Session
from models.offer import Offer
from models.geography import Geography


class OfferGeography(Base, BaseModel):
    """
    Модель для таблицы 'offer_geography'.
    Наследуется от BaseModel, включает базовые методы и поля.
    Переопределяет метод create для поиска внешних ключей по значению.
    """
    __tablename__ = "offer_geography"

    id_offer = Column(Integer, ForeignKey("offer.id"), nullable=False)
    id_geography = Column(Integer, ForeignKey("geography.id"), nullable=False)

    offer = relationship("Offer")
    geography = relationship("Geography")

    @classmethod
    def create(cls, offer_url, city, country):
        session = Session()

        offer = session.query(Offer).filter(Offer.url == offer_url).first()
        id_offer = offer.id if offer else -1

        geography = session.query(Geography).filter(Geography.city == city, Geography.country == country).first()
        id_geography = geography.id if geography else -1

        if cls.exists(id_offer=id_offer, id_geography=id_geography):
            print(f"OfferGeography with offer URL '{offer_url}' and geography '{city}, {country}' already exists!")
            return None

        offer_geography = cls(
            id_offer=id_offer,
            id_geography=id_geography
        )
        session.add(offer_geography)
        session.commit()
        session.refresh(offer_geography)
        return offer_geography

    def __repr__(self):
        return (f"<OfferGeography(id={self.id}, id_offer={self.id_offer}, "
                f"id_geography={self.id_geography})>")

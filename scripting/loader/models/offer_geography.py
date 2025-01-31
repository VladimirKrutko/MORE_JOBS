from scripting.loader.base_model import *
from scripting.loader.models.offer import Offer
from scripting.loader.models.geography import Geography


class OfferGeography(Base, BaseModel):
    __tablename__ = "offer_geography"

    id_offer = Column(Integer, ForeignKey("offer.id"), nullable=False)
    id_geography = Column(Integer, ForeignKey("geography.id"), nullable=False)

    offer = relationship("Offer")
    geography = relationship("Geography")

    @classmethod
    def create(cls, session, id_offer, id_geography):
        # session = Session()

        if cls.exists(id_offer=id_offer, id_geography=id_geography):
            print(f"OfferGeography with offer ID '{id_offer}' and geography ID '{id_geography}' already exists!")
            return None
        else:
            offer_geography = cls(
                id_offer=id_offer,
                id_geography=id_geography
            )
            session.add(offer_geography)
            session.commit()
            session.refresh(offer_geography)
            return offer_geography
        # offer = session.query(Offer).filter(Offer.url == offer_url).first()
        # id_offer = offer.id if offer else -1

        # geography = session.query(Geography).filter(Geography.city == city, Geography.country == country).first()
        # id_geography = geography.id if geography else -1

        # if cls.exists(id_offer=id_offer, id_geography=id_geography):
        #     print(f"OfferGeography with offer URL '{offer_url}' and geography '{city}, {country}' already exists!")
        #     return None

        # offer_geography = cls(
        #     id_offer=id_offer,
        #     id_geography=id_geography
        # )
        # session.add(offer_geography)
        # session.commit()
        # session.refresh(offer_geography)
        # return offer_geography

    def __repr__(self):
        return (f"<OfferGeography(id={self.id}, id_offer={self.id_offer}, "
                f"id_geography={self.id_geography})>")

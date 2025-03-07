from scripting.loader.models.technology import Technology
from scripting.loader.models.offer import Offer
from scripting.loader.base_model import *


class OfferTechnology(Base, BaseModel):
    __tablename__ = "offer_technology"

    id_offer = Column(Integer, ForeignKey("offer.id"), nullable=False)
    id_technology = Column(Integer, ForeignKey("technology.id"), nullable=False)
    obligatory = Column(Boolean, default=False)

    offer = relationship("Offer")
    technology = relationship("Technology")

    @classmethod
    def create(cls, session, id_offer, id_technology, obligatory=False):
        if session.query(OfferTechnology).filter(OfferTechnology.id_offer == id_offer, 
                                                 OfferTechnology.id_technology == id_technology,
                                                 OfferTechnology.obligatory == obligatory).first():
            print(f"OfferTechnology with offer ID '{id_offer}' and technology ID '{id_technology}' already exists!")
            return None
        else:
            offer_technology = cls(
                id_offer=id_offer,
                id_technology=id_technology,
                obligatory=obligatory
            )
            session.add(offer_technology)
            session.commit()
            session.refresh(offer_technology)
            return offer_technology
        # offer = session.query(Offer).filter(Offer.url == offer_url).first()
        # id_offer = offer.id if offer else -1

        # technology = session.query(Technology).filter(Technology.name == technology_name).first()
        # id_technology = technology.id if technology else -1

        # if cls.exists(id_offer=id_offer, id_technology=id_technology):
        #     print(f"OfferTechnology with offer '{offer_url}' and technology '{technology_name}' already exists!")
        #     return None

        # offer_technology = cls(
        #     id_offer=id_offer,
        #     id_technology=id_technology,
        #     obligatory=obligatory
        # )
        # session.add(offer_technology)
        # session.commit()
        # session.refresh(offer_technology)
        # return offer_technology

    def __repr__(self):
        return (f"<OfferTechnology(id={self.id}, id_offer={self.id_offer}, "
                f"id_technology={self.id_technology}, obligatory={self.obligatory})>")

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from MORE_JOBS.scripting.loader.base_model import BaseModel
from MORE_JOBS.scripting.loader.db_setup import Base, Session
from models.site import Site
from models.company import Company


class Offer(Base, BaseModel):
    __tablename__ = "offer"

    url = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    position_level = Column(String)
    id_data = Column(Integer, ForeignKey("offer_data.id"), nullable=True)
    site_id = Column(Integer, ForeignKey("site.id"), nullable=False)
    id_company = Column(Integer, ForeignKey("company.id"), nullable=False)
    active = Column(Boolean, default=True)

    site = relationship("Site")
    company = relationship("Company")
    offer_data = relationship("OfferData")

    @classmethod
    def create(cls, url, name, position_level=None, data_id=None, site_name=None, company_name=None, active=True):
        session = Session()

        site = session.query(Site).filter(Site.name == site_name).first()
        site_id = site.id if site else -1

        company = session.query(Company).filter(Company.name == company_name).first()
        id_company = company.id if company else -1

        id_data = data_id if data_id else -1

        if cls.exists(url=url):
            print(f"Offer with URL '{url}' already exists!")
            return None

        offer = cls(
            url=url,
            name=name,
            position_level=position_level,
            id_data=id_data,
            site_id=site_id,
            id_company=id_company,
            active=active
        )
        session.add(offer)
        session.commit()
        session.refresh(offer)
        return offer

    def __repr__(self):
        return (
            f"<Offer(id={self.id}, url='{self.url}', name='{self.name}', "
            f"site_id={self.site_id}",
            )

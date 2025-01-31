from scripting.loader.models.site import Site
from scripting.loader.models.company import Company
from scripting.loader.base_model import *

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
    def create(cls, session, url, name, position_level=None, site_id=None, id_data=None, company_id=None, active=True):
        # session = Session()

        site_id = site_id if site_id else -1

        # company = session.query(Company).filter(Company.name == company_name).first()
        company_id = company_id if company_id else -1

        id_data = id_data if id_data else -1
        offer_row = cls.exists(url=url)
        if offer_row:
            print(f"Offer with URL '{url}' already exists!")
            return offer_row

        offer = cls(
            url=url,
            name=name,
            position_level=position_level,
            id_data=id_data,
            site_id=site_id,
            id_company=company_id,
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

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from MORE_JOBS.scripting.loader.base_model import BaseModel, Session
from MORE_JOBS.scripting.loader.db_setup import Base
from models.salary import Salary
from models.offer import Offer


class OfferSalary(Base, BaseModel):
    __tablename__ = "offer_salary"

    id_salary = Column(Integer, ForeignKey("salary.id"), nullable=False)
    id_offer = Column(Integer, ForeignKey("offer.id"), nullable=False)

    salary = relationship("Salary")
    offer = relationship("Offer")

    @classmethod
    def create(cls, salary_value, salary_contract_type, offer_url):
        session = Session()

        salary = session.query(Salary).filter(
            Salary.value == salary_value, Salary.contract_type == salary_contract_type
        ).first()
        id_salary = salary.id if salary else -1

        offer = session.query(Offer).filter(Offer.url == offer_url).first()
        id_offer = offer.id if offer else -1

        if cls.exists(id_salary=id_salary, id_offer=id_offer):
            print(f"OfferSalary with salary '{salary_value}' and offer '{offer_url}' already exists!")
            return None

        offer_salary = cls(
            id_salary=id_salary,
            id_offer=id_offer
        )
        session.add(offer_salary)
        session.commit()
        session.refresh(offer_salary)
        return offer_salary

    def __repr__(self):
        return (f"<OfferSalary(id={self.id}, id_salary={self.id_salary}, "
                f"id_offer={self.id_offer})>")

from sqlalchemy import Column, String
from MORE_JOBS.scripting.loader.base_model import BaseModel
from MORE_JOBS.scripting.loader.db_setup import Base

class Salary(Base, BaseModel):
    __tablename__ = "salary"

    value = Column(String, nullable=False)
    contract_type = Column(String, nullable=True)

    def __repr__(self):
        return (f"<Salary(id={self.id}, value='{self.value}', "
                f"contract_type='{self.contract_type}')>")

from scripting.loader.base_model import *

class Company(Base, BaseModel):
    __tablename__ = "company"

    name = Column(String, nullable=False)
    url = Column(String)
    business_type = Column(String)
    description = Column(Text)

    def __repr__(self):
        return (f"<Company(id={self.id}, name='{self.name}', "
                f"url='{self.url}', business_type='{self.business_type}')>")

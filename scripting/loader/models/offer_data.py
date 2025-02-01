from scripting.loader.base_model import *


class OfferData(Base, BaseModel):
    __tablename__ = "offer_data"

    data = Column(JSON)
    requirements = Column(Text)
    responsibilities = Column(Text)
    original_language = Column(String)
    translated_data = Column(JSON)
    requirements_md5 = Column(Text)
    responsibilities_md5 = Column(Text)

    @classmethod
    def create(cls,session, **kwargs):
        offer_data = session.query(OfferData).filter(OfferData.requirements_md5 == kwargs["requirements_md5"], 
                                           OfferData.responsibilities_md5 == kwargs['responsibilities_md5']).first()
        if offer_data:
            print(f"OfferData with requirements MD5 '{kwargs['requirements_md5']}' and responsibilities MD5 '{kwargs['responsibilities_md5']}' already exists!")
            return offer_data
        
        offer_data = cls(**kwargs)
        session.add(offer_data)
        session.commit()
        session.refresh(offer_data)
        return offer_data

    def __repr__(self):
        return (f"<OfferData(id={self.id}, original_language='{self.original_language}', "
                f"requirements_length={len(self.requirements) if self.requirements else 0}, "
                f"responsibilities_length={len(self.responsibilities) if self.responsibilities else 0})>")

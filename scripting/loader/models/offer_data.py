from scripting.loader.base_model import *


class OfferData(Base, BaseModel):
    __tablename__ = "offer_data"

    data = Column(JSON)
    requirements = Column(Text)
    responsibilities = Column(Text)
    original_language = Column(String)
    translated_data = Column(JSON)

    @classmethod
    def create(cls, data=None, requirements=None, responsibilities=None, original_language=None, translated_data=None):
        session = Session()

        offer_data = cls(
            data=data,
            requirements=requirements,
            responsibilities=responsibilities,
            original_language=original_language,
            translated_data=translated_data
        )
        session.add(offer_data)
        session.commit()
        session.refresh(offer_data)
        return offer_data

    def __repr__(self):
        return (f"<OfferData(id={self.id}, original_language='{self.original_language}', "
                f"requirements_length={len(self.requirements) if self.requirements else 0}, "
                f"responsibilities_length={len(self.responsibilities) if self.responsibilities else 0})>")

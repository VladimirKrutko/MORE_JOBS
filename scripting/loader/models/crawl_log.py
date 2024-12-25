from scripting.loader.base_model import *

class CrawlLog(BaseModel):
    __tablename__ = 'crawl_log'

    url = Column(String, nullable=False)
    site = Column(String, nullable=False)
    status = Column(String, nullable=True)
    mode = Column(String, nullable=True)

    @classmethod
    def create(cls, **kwargs):
        session = Session()
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

from scripting.loader.base_model import *

class PageStatus(BaseModel):
    __tablename__ = 'page_status'

    url = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False)

    def add_or_update_page_status(session, url, status):
        page_status = session.query(PageStatus).filter_by(url=url).first()

        if page_status:
            page_status.status = status
            page_status.update_date = datetime.now()
        else:
            page_status = PageStatus(url=url, status=status)
            session.add(page_status)
        session.commit()
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    domain = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    description = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    offers = relationship("Offer", back_populates="company")

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('site.id'))
    url = Column(String)
    active = Column(Boolean)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    site = relationship("Site")

class PositionLevel(Base):
    __tablename__ = 'position_level'
    id = Column(Integer, primary_key=True)
    level = Column(String, unique=True)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class Offer(Base):
    __tablename__ = 'offer'
    id = Column(Integer)
    name = Column(String)
    id_company = Column(Integer, ForeignKey('company.id'))
    id_position_level = Column(Integer, ForeignKey('position_level.id'))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    __table_args__ = (PrimaryKeyConstraint('id', 'name', 'id_company'), )

    company = relationship("Company", back_populates="offers")
    position_level = relationship("PositionLevel")

class OfferLocation(Base):
    __tablename__ = 'offer_location'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey('offer.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    id_position_level = Column(Integer)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    offer = relationship("Offer")
    location = relationship("Location")

class Technology(Base):
    __tablename__ = 'technology'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class OfferTechnology(Base):
    __tablename__ = 'offer_technology'
    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    id_technology = Column(Integer, ForeignKey('technology.id'))
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    offer = relationship("Offer")
    technology = relationship("Technology")

class OfferData(Base):
    __tablename__ = 'offer_data'
    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    data = Column(JSON)
    id_original_language = Column(Integer, ForeignKey('language.id'))
    translated_data = Column(JSON)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    offer = relationship("Offer")
    language = relationship("Language")

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class OfferGeography(Base):
    __tablename__ = 'offer_geography'
    id = Column(Integer, primary_key=True)
    id_city = Column(Integer, ForeignKey('city.id'))
    id_country = Column(Integer, ForeignKey('country.id'))
    id_offer = Column(Integer, ForeignKey('offer.id'))
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    city = relationship("City")
    country = relationship("Country")
    offer = relationship("Offer")

class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class Salary(Base):
    __tablename__ = 'salary'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    contract_type = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class OfferSalary(Base):
    __tablename__ = 'offer_salary'
    id = Column(Integer, primary_key=True)
    id_salary = Column(Integer, ForeignKey('salary.id'))
    id_offer = Column(Integer, ForeignKey('offer.id'))
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    salary = relationship("Salary")
    offer = relationship("Offer")

class BussinesType(Base):
    __tablename__ = 'bussines_type'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

class CompanyBussinesType(Base):
    __tablename__ = 'company_bussines_type'
    id = Column(Integer, primary_key=True)
    id_company = Column(Integer, ForeignKey('company.id'))
    id_bussines_type = Column(Integer, ForeignKey('bussines_type.id'))
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    company = relationship("Company")
    bussines_type = relationship("BussinesType")

DATABASE_URL = "postgresql://username:password@localhost/yourdatabase"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

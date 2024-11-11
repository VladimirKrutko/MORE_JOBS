from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    domain = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    locations = relationship("Location", back_populates="site")

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    description = Column(Text)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offers = relationship("Offer", back_populates="company")
    business_types = relationship("CompanyBusinessType", back_populates="company")

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('site.id'))
    url = Column(String)
    active = Column(Boolean)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    site = relationship("Site", back_populates="locations")
    offer_locations = relationship("OfferLocation", back_populates="location")

class PositionLevel(Base):
    __tablename__ = 'position_level'

    id = Column(Integer, primary_key=True)
    level = Column(String, unique=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offers = relationship("Offer", back_populates="position_level")
    offer_locations = relationship("OfferLocation", back_populates="position_level")

class Offer(Base):
    __tablename__ = 'offer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_company = Column(Integer, ForeignKey('company.id'))
    id_position_level = Column(Integer, ForeignKey('position_level.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="offers")
    position_level = relationship("PositionLevel", back_populates="offers")
    offer_locations = relationship("OfferLocation", back_populates="offer")
    offer_technologies = relationship("OfferTechnology", back_populates="offer")
    offer_data = relationship("OfferData", back_populates="offer")
    offer_geographies = relationship("OfferGeography", back_populates="offer")
    offer_salaries = relationship("OfferSalary", back_populates="offer")

class OfferLocation(Base):
    __tablename__ = 'offer_location'

    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey('offer.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    id_position_level = Column(Integer, ForeignKey('position_level.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="offer_locations")
    location = relationship("Location", back_populates="offer_locations")
    position_level = relationship("PositionLevel", back_populates="offer_locations")

class Technology(Base):
    __tablename__ = 'technology'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer_technologies = relationship("OfferTechnology", back_populates="technology")

class OfferTechnology(Base):
    __tablename__ = 'offer_technology'

    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    id_technology = Column(Integer, ForeignKey('technology.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="offer_technologies")
    technology = relationship("Technology", back_populates="offer_technologies")

class OfferData(Base):
    __tablename__ = 'offer_data'

    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    data = Column(JSON)
    requirements = Column(Text)
    responsibilities = Column(Text)
    id_original_language = Column(Integer, ForeignKey('language.id'))
    translated_data = Column(JSON)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="offer_data")
    language = relationship("Language", back_populates="offer_data")

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer_data = relationship("OfferData", back_populates="language")

class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer_geographies = relationship("OfferGeography", back_populates="country")

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer_geographies = relationship("OfferGeography", back_populates="city")

class OfferGeography(Base):
    __tablename__ = 'offer_geography'

    id = Column(Integer, primary_key=True)
    id_city = Column(Integer, ForeignKey('city.id'))
    id_country = Column(Integer, ForeignKey('country.id'))
    id_offer = Column(Integer, ForeignKey('offer.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    city = relationship("City", back_populates="offer_geographies")
    country = relationship("Country", back_populates="offer_geographies")
    offer = relationship("Offer", back_populates="offer_geographies")

class Salary(Base):
    __tablename__ = 'salary'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    contract_type = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer_salaries = relationship("OfferSalary", back_populates="salary")

class OfferSalary(Base):
    __tablename__ = 'offer_salary'

    id = Column(Integer, primary_key=True)
    id_salary = Column(Integer, ForeignKey('salary.id'))
    id_offer = Column(Integer, ForeignKey('offer.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    salary = relationship("Salary", back_populates="offer_salaries")
    offer = relationship("Offer", back_populates="offer_salaries")

class BusinessType(Base):
    __tablename__ = 'business_type'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    company_business_types = relationship("CompanyBusinessType", back_populates="business_type")

class CompanyBusinessType(Base):
    __tablename__ = 'company_business_type'

    id = Column(Integer, primary_key=True)
    id_company = Column(Integer, ForeignKey('company.id'))
    business_type_id = Column(Integer, ForeignKey('business_type.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="business_types")
    business_type = relationship("BusinessType", back_populates="company_business_types")

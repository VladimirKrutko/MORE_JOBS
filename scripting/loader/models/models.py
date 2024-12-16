from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, DateTime, JSON
)
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


class Offer(Base):
    __tablename__ = 'offer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_company = Column(Integer, ForeignKey('company.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="offers")
    locations = relationship("OfferLocation", back_populates="offer")
    technologies = relationship("OfferTechnology", back_populates="offer")
    data = relationship("OfferData", back_populates="offer")
    salaries = relationship("OfferSalary", back_populates="offer")
    geographies = relationship("OfferGeography", back_populates="offer")
    responsibilities = relationship("OfferResponsibilities", back_populates="offer")
    requirements = relationship("OfferRequirements", back_populates="offer")


class OfferLocation(Base):
    __tablename__ = 'offer_location'

    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey('offer.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    id_position_level = Column(Integer)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="locations")
    location = relationship("Location", back_populates="offer_locations")


class Technology(Base):
    __tablename__ = 'technology'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offers = relationship("OfferTechnology", back_populates="technology")


class OfferTechnology(Base):
    __tablename__ = 'offer_technology'

    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    id_technology = Column(Integer, ForeignKey('technology.id'))
    obligatory = Column(Boolean)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="technologies")
    technology = relationship("Technology", back_populates="offers")


class OfferData(Base):
    __tablename__ = 'offer_data'

    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    data = Column(JSON)
    id_original_language = Column(Integer, ForeignKey('language.id'))
    translated_data = Column(JSON)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="data")
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

    geographies = relationship("OfferGeography", back_populates="country")


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    geographies = relationship("OfferGeography", back_populates="city")


class OfferGeography(Base):
    __tablename__ = 'offer_geography'

    id = Column(Integer, primary_key=True)
    id_city = Column(Integer, ForeignKey('city.id'))
    id_country = Column(Integer, ForeignKey('country.id'))
    id_offer = Column(Integer, ForeignKey('offer.id'))
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    city = relationship("City", back_populates="geographies")
    country = relationship("Country", back_populates="geographies")
    offer = relationship("Offer", back_populates="geographies")


class Responsibilities(Base):
    __tablename__ = 'responsibilities'

    id = Column(Integer, primary_key=True)
    data = Column(Text)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offers = relationship("OfferResponsibilities", back_populates="responsibilities")


class OfferResponsibilities(Base):
    __tablename__ = 'offer_responsibilities'

    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    id_responsibilities = Column(Integer, ForeignKey('responsibilities.id'))
    obligatory = Column(Boolean)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="responsibilities")
    responsibilities = relationship("Responsibilities", back_populates="offers")


class Requirements(Base):
    __tablename__ = 'requirements'

    id = Column(Integer, primary_key=True)
    data = Column(Text)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offers = relationship("OfferRequirements", back_populates="requirements")


class OfferRequirements(Base):
    __tablename__ = 'offer_requirements'

    id = Column(Integer, primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id'))
    id_requirements = Column(Integer, ForeignKey('requirements.id'))
    obligatory = Column(Boolean)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="requirements")
    requirements = relationship("Requirements", back_populates="offers")

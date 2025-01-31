from scripting.sys.sys_functions import read_s3_object
from scripting.loader.import_all_models import *
from scripting.loader.db_setup import Session
import hashlib
import json

"""
Class for loading data from s3 with parsed data into DWH
"""

class PageDataLoader:
    def __init__(self, s3_path):
        self.page_data = json.loads(read_s3_object(s3_path))

    def load_data(self):
        self.session = Session()
        dimension_data = self.load_dimension_data()
        self.load_fact_data(dimension_data)
        self.session.close()


    def load_dimension_data(self):
        geography_ids = self.load_geography_data()
        technology_ids = self.load_technology_data()
        offer_data_id = self.load_offer_data()
        company_id = self.load_company_data()
        return {
            "offer_data_id": offer_data_id,
            "geography_ids": geography_ids,
            "technology_ids": technology_ids,
            "company_id": company_id
        }
    
    def load_fact_data(self, dimension_data):
        offer_id = self.load_offer(dimension_data["offer_data_id"], dimension_data["company_id"])
        self.load_offer_geography(offer_id, dimension_data["geography_ids"])
        self.load_offer_technology(offer_id, dimension_data["technology_ids"])

    def load_geography_data(self):
        return [ Geography.create(session= self.session, 
                                  city=city, 
                                  country=self.page_data["country"][0]).id for city in self.page_data["city"]]

    def load_technology_data(self):
        return {
            "required": [Technology.create(session= self.session, name=tech).id for tech in self.page_data["technology_list"]["required"]] if self.page_data["technology_list"]["required"] else [],
            "optional": [Technology.create(session= self.session, name=tech).id for tech in self.page_data["technology_list"]["optional"]] if self.page_data["technology_list"]["optional"] else []
        }
    
    def load_offer_data(self):
        offer_data = OfferData.create(
            session= self.session,
            requirements= self.page_data['requirements'],
            responsibilities=self.page_data['responsibilities'],
            requirements_md5 = hashlib.md5(self.page_data['requirements'].encode()).hexdigest(),
            responsibilities_md5 = hashlib.md5(self.page_data['responsibilities'].encode()).hexdigest(),
            original_language = self.page_data['language'],
            translated_data = {}
        )
        return offer_data.id
    
    def load_company_data(self):
        company = Company.create(
            session= self.session,
            name=self.page_data['company_name'],
            url=self.page_data['company_url'],
            description=self.page_data['company_description']
        )
        return company.id
    
    def load_offer(self, offer_data_id, company_id):
        offer = Offer.create(
            session= self.session,
            url=self.page_data['url'],
            name=self.page_data['offer_title'],
            position_level= "@@@@".join([position['name'].lower() for position in self.page_data['position_level']]),
            id_data=offer_data_id,
            site_id=Site.exists(name=self.page_data['site']).id,
            company_id=company_id,
            active=True
        )
        return offer.id
    
    def load_offer_geography(self, offer_id, geography_ids):
        for geography_id in geography_ids:
            OfferGeography.create(
                session= self.session,
                id_offer=offer_id,
                id_geography=geography_id
            )
        
    def load_offer_technology(self, offer_id, techology_ids):
        for tech_id in techology_ids['required']:
            OfferTechnology.create(
                session= self.session,
                id_offer=offer_id,
                id_technology=tech_id,
                obligatory=True
            )
        
        for tech_id in techology_ids['optional']:
            OfferTechnology.create(
                session= self.session,
                id_offer=offer_id,
                id_technology=tech_id,
                obligatory=False
            )    
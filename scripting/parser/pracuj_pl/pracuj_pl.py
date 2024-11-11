import re
from parser.base_parser import *

class PracujPLParser(BaseParser):
    JSON_PATTERN = r"window\['kansas-offerview'\]\s*=\s*(\{.*?\});"
    def __init__(self, parsed_site):
        super().__init__(parsed_site)
        self.parse_result = {
            'site': self.parsed_site,
            'company_name': None,
            'company_url': None,
            'company_description': None,
            'offer_title': None,
            'position_level': None,
            'technology_list': None,
            'offer_description': None,
            'requirements': None,
            'responsibilities': None,
            'language': None,
            'city': None,
            'country': None,
            'salary': None,
            'business_type': None,
            }
    
    def initalize_variables(self, responce_result):
        self.doc = BeautifulSoup(responce_result, 'html.parser')
        self.base_json = self.extract_json("window['kansas-offerview']")
        self.full_json = self.extract_json("window['kansas-offerview']")
        self.offer_section = self.full_json['offerReducer']['offer']['sections']
        
    def parse(self, responce_result):
        self.initalize_variables(self, responce_result)
        self.parse_page(responce_result)
        return self.parse_result
    
    def parse_offer_data(self):
        self.parse_result['company_name'] = self.base_json['offerReducer']['offer']['employerName']
        self.parse_result['company_description'] = self.parse_company_description('')
        self.parse_result['offer_title'] = self.base_json['offerReducer']['offer']['jobTitle']
        self.parse_result['position_level'] = self.base_json['offerReducer']['offer']['positionLevels']
        self.parse_result['technology_list'] = self.parse_technology_list()
    
    def parse_technology_list(self):
        base_section = self.find_section(self.offer_section, 'technologies')
        technology_section = self.find_section(base_section['subSections'], 'technologies-expected')
        return [technology['name'] for technology in technology_section['model']['technologies']] if technology_section else None
        
    def parse_company_description(self):
        base_section = self.find_section(self.offer_section, 'companyDescription')
        desctiption_section = self.find_section(base_section['subSections'], 'about-us-description')
        return self.squish(" ".join(desctiption_section['model']['paragraphs'])) if desctiption_section else None
        
    def find_section(self, seection_list, section_name):
        return next((section for section in seection_list if section['sectionName'] == section_name), None)
        
    def squish(text):
        return re.sub(r'\s+', ' ', text).strip()
        
    def extract_json(self, tag_pattern):
        json_text = self.doc.find('script', id='__NEXT_DATA__').string
        return json.loads(json_text.replace("'", '"').replace('undefined', '"undefined"'))
    
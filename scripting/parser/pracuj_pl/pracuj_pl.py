import re
from parser.base_parser import *

class PracujPLParser(BaseParser):
    JSON_PATTERN = r"window\['kansas-offerview'\]\s*=\s*(\{.*?\});"
    def __init__(self, parsed_site):
        super().__init__(parsed_site)
        self.parsed_result = {
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
        
    JSON_PATHS = {
        'company_name': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'displayEmployerName'],
        'company_description': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'],
        'offer_title': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'jobTitle'],
        'position_level': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'positionLevels'],
        'technologies': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'textSections'],
    }
    
    def initalize_variables(self, responce_result, url):
        self.url = url
        self.doc = BeautifulSoup(responce_result, 'html.parser')
        self.page_json = self.extract_json()
        
    def parse(self, responce_result, url):
        self.initalize_variables(responce_result, url)
        self.parse_page(responce_result)
        return self.parsed_result
    
    def parse_offer_data(self):
        self.parsed_result['company_name'] = self.get_json_value(self.page_json, self.JSON_PATHS['company_name'])
        self.parsed_result['company_description'] = self.parse_company_description()
        self.parsed_result['offer_title'] = self.get_json_value(self.page_json, self.JSON_PATHS['offer_title'])
        self.parsed_result['position_level'] = self.get_json_value(self.page_json, self.JSON_PATHS['position_level'])
        self.parsed_result['technology_list'] = self.parse_technology_list()
        self.parsed_result['offer_description'] = ''
        # self.parse_offer_description()
    
    def parse_technology_list(self):
        technology_list = {}
        offer_technologies = self.get_json_value(self.page_json, self.JSON_PATHS['technologies'])
        get_techology = lambda tesh: next((tech for tech in offer_technologies if tech['sectionType'] == tesh), {})
        technology_list['required'] = get_techology('technologies-expected').get('textElements')
        technology_list['expected'] = get_techology('technologies-optional').get('textElements')
        return technology_list
        # next((tech for tech in offer_technologies if tech['sectionType'] == 'technologies-expected'), None)['textElements']
        # base_section = self.find_section(self.offer_section, 'technologies')
        # technology_section = self.find_section(base_section['subSections'], 'technologies-expected')
        # return [technology['name'] for technology in technology_section['model']['technologies']] if technology_section else None
        
    def parse_company_description(self):
        base_section = self.get_json_value(self.page_json, self.JSON_PATHS['company_description'])
        desctiption_section = self.find_section(base_section, 'about-us-description')
        return self.squish(" ".join(desctiption_section['model']['paragraphs'])) if desctiption_section else None
        
    def find_section(self, seection_list, section_name):
        return next((section for section in seection_list if section['sectionName'] == section_name), None)
        
    def squish(text):
        return re.sub(r'\s+', ' ', text).strip()
        
    def extract_json(self):
        json_text = self.doc.find('script', id='__NEXT_DATA__').string
        return json.loads(json_text.replace("'", '"').replace('undefined', '"undefined"'))
    
    def get_json_value(self, json_obj, json_path, key_index=0):
        try:
            return self.get_offer_value(json_obj[json_path[key_index]], json_path, key_index + 1)
        except:
            return json_obj
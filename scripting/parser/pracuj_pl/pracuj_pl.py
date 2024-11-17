import re
from parser.base_parser import *

class PracujPLParser(BaseParser):
    JSON_PATTERN = r"window\['kansas-offerview'\]\s*=\s*(\{.*?\});"
    RESULT_TEMPLATE ={
            'url': None,
            'site': 'pracuj.pl',
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
            'salary': None,
            'work_type': None,
            }
    WORKING_TIME = 8
    WORKING_DAYS = 20
    
    def __init__(self, parsed_site):
        super().__init__(parsed_site)
        
    JSON_PATHS = {
        'company_name': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'displayEmployerName'],
        'company_description': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'],
        'offer_title': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'jobTitle'],
        'position_level': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'positionLevels'],
        'technologies': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'textSections'],
        'requairemtns': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'],
        'responsibilities': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'],
        'language': ['props', 'pageProps', 'langCode'],
        'salary': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'typesOfContracts'],
        'work_type': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'workModes'],
        'locaiton': ['props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'workplaces'],
    }
    
    def initalize_variables(self, page_content, url):
        self.url = url
        self.doc = BeautifulSoup(page_content, 'html.parser')
        self.page_json = self.extract_json()
        
    def parse(self, page_content, url):
        result = self.RESULT_TEMPLATE.copy()
        self.initalize_variables(page_content, url)
        self.parse_offer_data(result)
        return result
    
    def parse_offer_data(self, result):
        result['url'] = self.url
        result['company_name'] = self.get_json_value(self.page_json, self.JSON_PATHS['company_name'])
        result['company_description'] = self.parse_company_description()
        result['offer_title'] = self.get_json_value(self.page_json, self.JSON_PATHS['offer_title'])
        result['position_level'] = self.get_json_value(self.page_json, self.JSON_PATHS['position_level'])
        result['technology_list'] = self.parse_technology_list()
        result['requirements'] = self.parse_rr_section('requirements')
        result['responsibilities'] = self.parse_rr_section('responsibilities')
        result['language'] = self.get_json_value(self.page_json, self.JSON_PATHS['language'])
        result['salary'] = self.parse_salary()
        result['work_type'] = self.get_json_value(self.page_json, self.JSON_PATHS['salary'])
        result['city'] = self.parse_location(self, 'city')
        result['country'] = self.parse_location(self, 'country')
    
    def parse_location(self, location_type):
        location_data = self.get_json_value(self.page_json, self.JSON_PATHS['locaiton'])
        location_result = set()
        for location in location_data:
            match location_type:
                case 'city':
                    location_result.add(location['inlandLocation']['location']['name'])
                case 'country':
                    location_result.add(location['inlandLocation']['location']['country']['name'])
                case _:
                    location_result.add(None)
        return location_result                            

    def parse_work_type(self):
        work_type = self.get_json_value(self.page_json, self.JSON_PATHS['work_type'])
        return [wt['code'] for wt in work_type] if work_type else None
    
    def parse_salary(self):
        salary_data = self.get_json_value(self.page_json, self.JSON_PATHS['salary'])
        process_salary = lambda salary: {
            'salary_amount': self.salary_amount(salary), 
            'employment_type': salary['name'], 
            'currency': salary['currency']['code']
            }
        return list(map(process_salary, salary_data)) if salary_data else None
    
    def salary_amount(self, salary):
        salary_amount = (
            f"{salary['from'] * self.WORKING_TIME * self.WORKING_DAYS}-{salary['to'] * self.WORKING_TIME * self.WORKING_DAYS}"
            if salary['timeUnit']['shortForm'] in ('godz', 'h') or 'h' in salary['timeUnit']['shortForm']
            else f"{salary['from']}-{salary['to']}"
        )
        return salary_amount        

    def parse_rr_section(self, section_name):
        base_section = self.get_json_value(self.page_json, self.JSON_PATHS['company_description'])
        desctiption_section = self.find_section(base_section, section_name)
        return self.squish(" ".join(desctiption_section['model']['paragraphs'])) if desctiption_section else None
    
    def parse_technology_list(self):
        technology_list = {}
        offer_technologies = self.get_json_value(self.page_json, self.JSON_PATHS['technologies'])
        get_techology = lambda tesh: next((tech for tech in offer_technologies if tech['sectionType'] == tesh), {})
        technology_list['required'] = get_techology('technologies-expected').get('textElements')
        technology_list['expected'] = get_techology('technologies-optional').get('textElements')
        return technology_list
        
    def parse_company_description(self):
        base_section = self.get_json_value(self.page_json, self.JSON_PATHS['company_description'])
        desctiption_section = self.find_section(base_section, 'about-us-description')
        return self.squish(" ".join(desctiption_section['model']['paragraphs'])) if desctiption_section else None
        
    def find_section(self, seection_list, section_name):
        return next((section for section in seection_list if section['sectionType'] == section_name), None)
        
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
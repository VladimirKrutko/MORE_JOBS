from .base_methods import BaseMethods
from scripting.shop_modules.base_parser import *

class Parser(BaseParser, BaseMethods):
    JSON_PATTERN = r"window\['kansas-offerview'\]\s*=\s*(\{.*?\});"
    WORKING_TIME = 8
    WORKING_DAYS = 20
    JSON_PATHS = {
        'company_name': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'displayEmployerName'),
        'company_description': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'),
        'offer_title': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'jobTitle'),
        'position_level': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'positionLevels'),
        'technologies': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'textSections'),
        'requirements': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'),
        'responsibilities': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'),
        'language': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'jobOfferLanguage', 'isoCode'),
        'salary': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'typesOfContracts'),
        'work_type': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'workModes'),
        'location': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'workplaces'),
    }

    def __init__(self, parsed_site):
        super().__init__(parsed_site)

    def parse(self, page_content, url):
        result = self.RESULT_TEMPLATE.copy()
        self.initialize_variables(page_content, url)
        self.parse_offer_data(result)
        return self.process_result(result)

    def parse_offer_data(self, result):
        result.update({
            'url': self.url,
            'company_name': self.get_json_value(self.page_json, self.JSON_PATHS['company_name']),
            'company_description': self.parse_company_description(),
            'offer_title': self.get_json_value(self.page_json, self.JSON_PATHS['offer_title']),
            'position_level': self.get_json_value(self.page_json, self.JSON_PATHS['position_level']),
            'technology_list': self.parse_technology_list(),
            'offer_description': self.parse_offer_description(),
            'requirements': self.parse_rr_section('requirements'),
            'responsibilities': self.parse_rr_section('responsibilities'),
            'language': self.get_json_value(self.page_json, self.JSON_PATHS['language']),
            'salary': self.parse_salary(),
            'work_type': self.parse_work_type(),
            'city': self.parse_location('city'),
            'country': self.parse_location('country'),
        })

    def parse_work_type(self):
        work_type = self.get_json_value(self.page_json, self.JSON_PATHS['work_type'])
        return [wt['code'] for wt in work_type] if work_type else None

    def parse_location(self, location_type):
        location_data = self.get_json_value(self.page_json, self.JSON_PATHS['location'])
        location_result = set()

        for location in location_data:
            if location_type == 'city':
                location_result.add(location['inlandLocation']['location']['name'])
            elif location_type == 'country':
                location_result.add(location['country']['name'])
            else:
                location_result.add(None)
        return location_result

    def parse_offer_description(self):
        desc_section = self.find_section(self.get_json_value(self.page_json, self.JSON_PATHS['company_description']), 'about-project')
        return self.squish(" ".join(desc_section['model']['paragraphs']))
    
    def parse_salary(self):
        salary_data = self.get_json_value(self.page_json, self.JSON_PATHS['salary'])
        if salary_data[0]['salary'] is None:
            return '-'

        process_salary = lambda salary: {
            'salary_amount': self.salary_amount(salary['salary']),
            'employment_type': salary['name'],
            'currency': salary['salary']['currency']['code']
        }
        return list(map(process_salary, salary_data)) if salary_data else None

    def salary_amount(self, salary):
        if salary is None:
            return '-'
        return (
            f"{salary['from'] * self.WORKING_TIME * self.WORKING_DAYS}-{salary['to'] * self.WORKING_TIME * self.WORKING_DAYS}"
            if salary['timeUnit']['longForm']['name'] != 'monthly'
            else f"{salary['from']}-{salary['to']}"
        )

    def parse_rr_section(self, section_name):
        base_section = self.get_json_value(self.page_json, self.JSON_PATHS['company_description'])
        description_section = self.find_section(base_section, section_name)
        join_bullets = lambda section: "@@@@".join(section['model']['bullets'])

        if description_section.get('subSections'):
            return "@@@@".join(
                [join_bullets(sub_section) for sub_section in description_section['subSections']]
            ) if description_section else None
        return join_bullets(description_section) if description_section else None
    
    def parse_technology_list(self):
        technology_list = {}
        offer_technologies = self.get_json_value(self.page_json, self.JSON_PATHS['technologies'])
        get_technology = lambda tech: next(
            (t for t in offer_technologies if t['sectionType'] == tech), {}
        )

        technology_list['required'] = get_technology('technologies-expected').get('textElements')
        technology_list['optional'] = get_technology('technologies-optional').get('textElements')
        return technology_list

    def parse_company_description(self):
        base_section = self.get_json_value(self.page_json, self.JSON_PATHS['company_description'])
        description_section = self.find_section(base_section, 'about-us-description')
        return self.squish(" ".join(description_section['model']['paragraphs'])) if description_section else None

    def find_section(self, section_list, section_name):
        return next((section for section in section_list if section['sectionType'] == section_name), None)

    def extract_json(self):
        json_text = self.doc.find('script', id='__NEXT_DATA__').string
        return json.loads(json_text.replace("'", '"').replace('undefined', '"undefined"'))
    
    def get_json_value(self, json_obj, json_path, key_index=0):
        try:
            return self.get_json_value(json_obj[json_path[key_index]], json_path, key_index + 1)
        except (IndexError, KeyError, TypeError):
            return json_obj

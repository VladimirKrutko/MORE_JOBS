from scripting.sys.sys_functions import SQS_CLIENT, OLLAMA_HOST
from scripting.loader.models.offer_data import OfferData
from scripting.sys.aws_variables import SQS_LOADER
from scripting.loader.db_setup import Session
from scripting.sys.static_meta import StaticMeta
import requests
import json
from deep_translator import GoogleTranslator

class DataProcessing(metaclass=StaticMeta):

    def get_sqs_loader_message():
        response = SQS_CLIENT.receive_message(
            QueueUrl=SQS_LOADER,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,
            AttributeNames=['All'],
            MessageAttributeNames=['All']
        )
        return [message for message in response['Messages']] if 'Messages' in response else []
    
    def get_offer_data(offer_ids: list):
        session = Session()
        offer_data = session.query(OfferData).filter(OfferData.id.in_(offer_ids)).all()
        session.close()
        return offer_data
    
    def translate_data(offer_data_ids):
        session = Session()
        translater = GoogleTranslator(source='auto', target='english')

        offer_data = DataProcessing.get_offer_data(offer_data_ids)
        for offer in offer_data:
            updated_data = dict()
            for filed in ['requirements', 'responsibilities']:
                # prompt_text = DataProcessing.llama_translate_template(offer.__dict__[filed],)
                updated_data[filed] = translater.translate(offer.__dict__[filed])
                # DataProcessing.llama_request(prompt_text)
            OfferData.update(session, offer.id, **{'translated_data': updated_data})
        session.close()
        

    def llama_translate_template(translated_data, language='polish'):
        return f"just traslate text from {language} to english (return only translated text): {translated_data}"

    def llama_request(prompt_text):
        payload = {
            "model": "llama3.1",
            "prompt": prompt_text,
        }
        response = requests.post(OLLAMA_HOST, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        list_dict_words = []
        if response.status_code == 200:
            list_dict_words = []
            for each_word in response.text.split("\n"):
                try:
                    data = json.loads(each_word) 
                except:
                    pass
                list_dict_words.append(data)
        return "".join([word['response'] for word in list_dict_words if type(word) == type({})])

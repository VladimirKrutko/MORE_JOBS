from scripting.sys.static_meta import StaticMeta
from scripting.sys.sys_functions import CHROMA_DB_CLIENT

class ChromaDataLoader(metaclass=StaticMeta):

    def create_document(data):
        doc = f"""
        requrement: {data['requirements']}\n
        responsibilities: {data['responsibilities']}\n
        technology: {data['technologies']}\n
        company: {data['company']}\n
        salary: {data['salary']}\n
        """
        return doc

    def put_data_to_chroma_db(data):
        CHROMA_DB_CLIENT.put_data(data)
    # def

    # def __init__(self, **kwargs):
    #     self.kwargs = kwargs

    # def load_data(self):
    #     # Load data from source
    #     pass

    # def transform_data(self):
    #     # Transform data
    #     pass

    # def save_data(self):
    #     # Save data to destination
    #     pass

    # def run(self):
    #     self.load_data()
    #     self.transform_data()
    #     self.save_data()
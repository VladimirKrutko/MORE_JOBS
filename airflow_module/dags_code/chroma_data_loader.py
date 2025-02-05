from scripting.sys.sys_functions import CHROMA_DB_CLIENT, CHROMA_COLLECTION_NAME
from scripting.sys.sys_functions import logging, configure_logging
from scripting.loader.chroma_db import chroma_collection
from scripting.sys.static_meta import StaticMeta
from scripting.loader.db_setup import Session
from langchain_ollama import OllamaEmbeddings
import itertools

configure_logging()

class ChromaDataLoader(metaclass=StaticMeta):
    
    SQL_OFFER_QUERY = """
                        SELECT
                            o.id,
                            o.name,
                            od.responsibilities,
                            od.requirements,
                            od.translated_data,
                            COALESCE(string_agg(t.name, ', '), '') AS technologies,
                            c.name AS company,
                            COALESCE(s.value, '') AS salary
                        FROM offer o
                        JOIN offer_data od ON o.id_data = od.id
                        JOIN company c ON o.id_company = c.id
                        LEFT JOIN offer_salary os ON o.id = os.id_offer
                        LEFT JOIN salary s ON s.id = os.id_salary
                        LEFT JOIN offer_technology ot ON ot.id_offer = o.id
                        LEFT JOIN technology t ON t.id = ot.id_technology
                        WHERE o.id  IN :offer_ids
                        GROUP BY o.id, o.name, od.responsibilities, od.requirements, od.translated_data, c.name, s.value;
                    """
    
    SQL_CHROMA_QUERY = """
    SELECT
        o.id,
        o.name,
        od.responsibilities,
        od.requirements,
        od.translated_data,
        COALESCE(string_agg(t.name, ', '), '') AS technologies,
        c.name AS company,
        COALESCE(s.value, '') AS salary
    FROM offer o
    JOIN offer_data od ON o.id_data = od.id
    JOIN company c ON o.id_company = c.id
    LEFT JOIN offer_salary os ON o.id = os.id_offer
    LEFT JOIN salary s ON s.id = os.id_salary
    LEFT JOIN offer_technology ot ON ot.id_offer = o.id
    LEFT JOIN technology t ON t.id = ot.id_technology
    WHERE od.translated_data <> '{}' or od.original_language = 'en'
    GROUP BY o.id, o.name, od.responsibilities, od.requirements, od.translated_data, c.name, s.value;
    """

    COLUMN_NAMES = ['id', 'name', 'responsibilities','requirements', 'translated_data', 'technologies', 'company', 'salary']
    def execute_query(offer_ids: list):
        session = Session()
        result = session.execute(ChromaDataLoader.SQL_OFFER_QUERY, {'offer_ids': tuple(offer_ids)})
        session.close()
        return [dict(zip(ChromaDataLoader.COLUMN_NAMES, row)) for row in result]

    def document_template(data: dict):
        doc = f"""
        name: {data['name']}\n
        requirements: {data['translated_data']['requirements'] if data['translated_data'] else data['requirements'] }\n
        responsibilities: { data['translated_data']['responsibilities'] if data['translated_data'] else data['responsibilities'] }\n
        technology: {data['technologies']}\n
        company: {data['company']}\n
        salary: {data['salary']}
        """
        return doc

    def create_chroma_data(offer_ids: list)->list:
        query_result = ChromaDataLoader.execute_query(offer_ids)
        return [ (str(qr['id']), ChromaDataLoader.document_template(qr)) for qr in query_result ]
        
    def put_data_into_chroma_db(offer_ids: list):
        chroma_collection = CHROMA_DB_CLIENT.get_or_create_collection(CHROMA_COLLECTION_NAME)
        chroma_data = ChromaDataLoader.create_chroma_data(offer_ids)
        chroma_collection.add(
            documents=[offer[-1] for offer in chroma_data],
            ids=[offer[0] for offer in chroma_data]
        )

    def chunk_list(input_list, chunk_size=10):
        return [list(itertools.islice(input_list, i, i + chunk_size)) for i in range(0, len(input_list), chunk_size)]

    def all_offer_data_in_chroma_format():
        session = Session()
        offer_data = session.execute(ChromaDataLoader.SQL_CHROMA_QUERY).all()
        session.close()
        chroma_data = [ (str(od['id']), ChromaDataLoader.document_template(od)) for od in offer_data ]
        return ChromaDataLoader.chunk_list(chroma_data)

    def put_data_to_chroma_db_from_db():
        chroma_data = ChromaDataLoader.all_offer_data_in_chroma_format()
        logging.info(f"Total number of offers: {len(chroma_data)}")
        for chunk in chroma_data:
            chroma_collection.add(
                documents=[offer[-1] for offer in chunk],
                ids=[offer[0] for offer in chunk]
            )
            logging.info(f"Offer data inserted: {len(chunk)}")
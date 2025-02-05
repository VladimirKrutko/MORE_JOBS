from scripting.sys.sys_functions import send_message_to_sqs, delete_message_from_sqs, logging, configure_logging
from airflow_module.dags_code.chroma_data_loader import ChromaDataLoader
from scripting.sys.aws_variables import SQS_LOADER, SQS_ERORR_LOADER
from airflow_module.dags_code.page_data_loader import PageDataLoader
from airflow_module.dags_code.data_processing import DataProcessing
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
import json

configure_logging()

SQS_QUEUE_URL = "https://sqs.eu-central-1.amazonaws.com/123456789012/my-queue"

def get_messages_from_sqs(**kwargs):
    messages = DataProcessing.get_sqs_loader_message()
    if messages:
        logging.info(f"Get {len(messages)} messages from SQS")
        kwargs["ti"].xcom_push(key="messages", value=messages)
    else:
        logging.info("No messages in SQS")
        raise Exception("No messages in SQS")

def load_page_data_from_sqs_message(**kwargs):
    messages = kwargs["ti"].xcom_pull(key="messages", task_ids="get_messages_from_sqs")
    loader = PageDataLoader()
    offer_ids = []
    offer_data_ids = []
    for message in messages:
        message_data = json.loads(message.get("Body").replace("'", '"'))
        s3_path = message_data.get("s3_path")
        logging.info(f"Get message with path: {s3_path}")
        load_result = {}
        try:
            load_result = loader.load_data(s3_path)
            logging.info(f"Data from {s3_path} loaded.")
            delete_message_from_sqs(SQS_LOADER, message.get("ReceiptHandle"))
            offer_ids.append(load_result.get("offer_id"))
            offer_data_ids.append(load_result.get("offer_data_id"))
        except Exception as e:
            logging.error(f"Error loading data from {s3_path}: {e}")
            send_message_to_sqs(SQS_ERORR_LOADER, str(message_data))
    kwargs["ti"].xcom_push(key="offer_id", value=offer_ids)

def load_data_into_chroma_db(**kwargs):
    offer_id = kwargs["ti"].xcom_pull(key="offer_id", task_ids="load_page_data")
    logging.info(f"load_data_into_chroma_db -> Offer id: {offer_id}")
    if offer_id:
        ChromaDataLoader.put_data_into_chroma_db([offer_id] )
    else:
        logging.info("No offer id to load into chroma db")

dag = DAG(
    "sqs_triggered_data_loader",
    description="DAG to read load messages from SQS",
    schedule_interval = timedelta(seconds=240),
    start_date=datetime(2023, 1, 1),
    catchup=False
)

get_messages_task = PythonOperator(
    task_id="get_messages_from_sqs",
    python_callable=get_messages_from_sqs,
    provide_context=True,
    dag=dag
)

load_data_task = PythonOperator(
    task_id="load_page_data",
    python_callable=load_page_data_from_sqs_message,
    provide_context=True,
    execution_timeout=timedelta(minutes=15), 
    dag=dag
)

load_data_into_chroma_db_task = PythonOperator(
    task_id="load_data_into_chroma_db",
    python_callable=load_data_into_chroma_db,
    provide_context=True,
    dag=dag
)

get_messages_task >> load_data_task >> load_data_into_chroma_db_task
from airflow_module.dags_code.data_processing import DataProcessing
from scripting.loader.db_setup import Session
import signal
import sys

session = Session()

def signal_handler(signum, frame):
    session.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    DataProcessing.translate_offer_data(session=session)
    session.close()
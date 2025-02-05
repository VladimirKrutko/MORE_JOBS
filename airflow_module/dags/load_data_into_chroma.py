from scripting.sys.sys_functions import logging, configure_logging
from airflow_module.dags_code.chroma_data_loader import ChromaDataLoader
from scripting.sys.aws_variables import SQS_LOADER, SQS_ERORR_LOADER
from airflow_module.dags_code.data_processing import DataProcessing
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
import json


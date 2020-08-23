import sys
from os.path import dirname
sys.path.append(dirname(__file__))
import logging
from configparser import ConfigParser
from app.getcurrency import CurrencyDownloader
from app.getcurrency import InsightCalculator
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

config = ConfigParser()
config.read('./config/config.ini')
durl = config.get('URLS', 'DURL')
wurl = config.get('URLS', 'WURL')

PIPELINE_ID = 1

start_date = datetime(2020, 8, 22)

# Dag Arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_date,
   # 'email': ['sidgk248@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

# Dag Definition, Defining the dag
dag = DAG(
    dag_id='currency_api_fetch_dag',
    schedule_interval="0 * * * *",
    default_args=default_args,
    catchup=False)

# Creating the instance and calling the CurrencyDownloader function from getcurrency.py file
def downloadfile():
    reviewsDownloader = CurrencyDownloader(durl, wurl)
    reviewsDownloader.checkAndDownloadData()

# Creating the instance and calling the InsightCalculator function from getcurrency.py file
def calculateInsights():
    insightCalculator = InsightCalculator()
    insightCalculator.calculate_insights()

# main() function and log and save all the actions in myapp.log file created under logs folder
def main():
    logging.basicConfig(format='%(levelname)s %(asctime)s :: %(message)s',filename='./logs/myapp.log', level=logging.INFO)
    logging.info('Starting application...')
    downloadfile()
    calculateInsights()
    logging.info('Application Finished.')

#Create a task to download data
convert_currency =  PythonOperator(
    task_id='load_stockprice_to_CSV',
    python_callable=downloadfile,
    dag=dag)
#Create a task to do the calculations
perform_calculations =  PythonOperator(
    task_id='load_stockprice_to_CSV',
    python_callable=calculateInsights,
    dag=dag)
#Created dummy task to explain Dependencies section.
t_first_task = DummyOperator(
    task_id='first_task',
    dag=dag
)

# Set dependency, Downstream dependency is set, i.e. Tasks begin to execute from Left to Right
t_first_task >> convert_currency >> perform_calculations

if __name__ == "__main__":
    main()
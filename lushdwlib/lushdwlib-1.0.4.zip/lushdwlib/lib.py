import config
import requests
import json
import os
import time
import re
import sys
import datetime
from os import path
from datetime import timedelta
from google.cloud import bigquery
import logging
import logging.handlers
from slackclient import SlackClient
from environs import Env
from datetime import timedelta
import uuid


#env = Env()
#env.read_env()
#SLACK_TOKEN=env("SLACK_TOKEN")
SLACK_TOKEN=os.environ.get('SLACK_TOKEN')
SMTP_EMAIL=os.environ.get('SMTP_EMAIL')
EMAIL_FROM=os.environ.get('EMAIL_FROM')
EMAIL_TO=os.environ.get('EMAIL_TO')

#BASIC CONFIGURATION
UUID = uuid.uuid4().hex


#LOGGING CONFIGURATION
LOG_FILE = 'LOG.json'
LOG_DATASET_ID = 'social_media'
LOG_TABLE_ID = 'projects_log'

#########################################################################################
#Error handling - Email Configuration                                                   #
#########################################################################################
EMAIL_HOST = SMTP_EMAIL                                                   #
EMAIL_PORT = 587                                                                        #
EMAIL_SUBJECT = "Python script issue 😱 - Have a look and fix it 🖖"
EMAIL_FROM = EMAIL_FROM                                                #
EMAIL_TO = EMAIL_TO
#########################################################################################


#LOGGER##########################################################################################################

#LOGGING TO THE FILE
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename=LOG_FILE,
                            filemode='w',
                            format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)

#EMAIL AN ERROR
logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)
smtp_handler = logging.handlers.SMTPHandler(mailhost=(EMAIL_HOST, EMAIL_PORT),
                                            fromaddr=EMAIL_FROM, 
                                            toaddrs=EMAIL_TO, 
                                            subject=EMAIL_SUBJECT) 

logger = logging.getLogger()


def current_timestamp():
    time.sleep(1)
    CURRENT_TIME = time.time()
    CURRENT_TIMESTAMP = datetime.datetime.fromtimestamp(CURRENT_TIME).strftime('%Y-%m-%d %H:%M:%S')
    return CURRENT_TIMESTAMP


#Modify JSON File, that BQ will accept it.
def modify_log_file(FILE_NAME,PROJECT):
    print("Ready to remove issues from {} file".format(FILE_NAME))

    with open(FILE_NAME, "r") as infileFollow:
        data = infileFollow.read()\
        .replace(' root ', '","level":"root","message":"')\
        .replace(' oauth2client.transport ', '","level":"oauth2client.transport","message":"')\
        .replace(' oauth2client.client ', '","level":"oauth2client.client","message":"')\
        .replace('\n','", "flag":""}\n')\
        .replace('#####", "flag":""','#####", "flag":"100"')\
        .replace(' googleapiclient.http WARNING','","level":"root","message":"googleapiclient.http WARNING')\
        .replace('">','>')\
        .replace('"The','The')\
        .replace('"teamDriveMembershipRequired"','teamDriveMembershipRequired')
        mod_data = re.sub('(^)', '{'+'"uuid":"{}","project":"{}","date":"'.format(UUID, PROJECT), data, flags = re.M)

    with open(FILE_NAME, "w+") as outfileFollow:
        outfileFollow.write(mod_data)

    CURRENT_TIMESTAMP = current_timestamp()
    with open(FILE_NAME, "a") as myfile:
        myfile.write('{}","level":"root","message":"INFO #############{}#############", "flag":"100"'.format(CURRENT_TIMESTAMP,PROJECT)+'}')

    print("File: {} modified - removed all the known issues".format(FILE_NAME)) 



#LOGGER##########################################################################################################





#PROJECTS##########################################################################################################

def logger_header(PROJECT):
    logger.info('#############{}#############'.format(PROJECT)) 
    time.sleep(1)


def project_auth(SERVICE_KEY):
    BQKEY = path.join('/auth/', SERVICE_KEY)

    #GOOGLE ENVIROMENTAL SERVICE KEY
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = BQKEY 
    return BQKEY

def clean_file(FILE):
    open(FILE, 'w').close()



#Upload LOG FILE TO BIGQUERY
def upload_log(FILE_NAME):
    client = bigquery.Client()
 
    dataset_ref = client.dataset(LOG_DATASET_ID)
    table_ref = dataset_ref.table(LOG_TABLE_ID)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    #job_config.skip_leading_rows = 1
    job_config.autodetect = False

    with open(FILE_NAME, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location='EU',  # Must match the destination dataset location.
            job_config=job_config)  # API request

    job.result()  # Waits for table load to complete.


def slack_message(message, channel):
    token = SLACK_TOKEN
    sc = SlackClient(token)
    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='@PythonBot',
                icon_emoji=':snake:')

    

def log_result_error(e):
    logger.addHandler(smtp_handler)
    time.sleep(1)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.error('OOPS! There is an issue in the {}: {}'.format(config.PROJECT_NAME,str(e)))
    slack_message('-------------------------------------- \n *Project name:* {} \n *Working path:* "{}" \n *Error type*:{} \n *Error:* {} \n *File name:* {} \n *Line:* {} \n *Logging:* {} \n--------------------------------------'\
            .format(config.PROJECT_NAME, os.getcwd(), exc_type, str(e), fname, exc_tb.tb_lineno,'https://bit.ly/2Er5yP2'),'#test-python')
    print(str(e))
    modify_log_file(LOG_FILE, config.PROJECT_NAME)
    upload_log(LOG_FILE)

def log_result_pass():
    modify_log_file(LOG_FILE, config.PROJECT_NAME)
    upload_log(LOG_FILE)


def log_result_error_c(PROJECT_NAME,e):
    logger.addHandler(smtp_handler)
    time.sleep(1)
    logger.error('OOPS! There is an issue in the {}: {}'.format(PROJECT_NAME,str(e)))
    slack_message('-------------------------------------- \n *Project name:* {} \n *Working path:* "{}" \n *Error type*:{} \n *Error:* {} \n *File name:* {} \n *Line:* {} \n--------------------------------------'\
            .format(PROJECT_NAME,str(e),os.getcwd()),'#test-python')
    print(str(e))
    modify_log_file(LOG_FILE, PROJECT_NAME)
    upload_log(LOG_FILE)

def log_result_pass_c(PROJECT_NAME):
    modify_log_file(LOG_FILE, PROJECT_NAME)
    upload_log(LOG_FILE)








def bq_remove_more_than(TABLE_NAME, DATASET_ID, TABLE_ID, WHERE, MORE_THAN):
    #Remove existing table ( empty the table )
    client = bigquery.Client()
    query = ('DELETE FROM `{}.{}.{}` WHERE {} >= "{}" '.format(TABLE_NAME,DATASET_ID,TABLE_ID,WHERE,MORE_THAN))
    query_job = client.query(query,location='EU')
    query_job.result()
    logger.info('Affected {} rows | Table {}:{}:{} truncated'.format(query_job.num_dml_affected_rows,TABLE_NAME,DATASET_ID,TABLE_ID))


def bq_remove_full(TABLE_NAME, DATASET_ID, TABLE_ID):
    #Remove existing table ( empty the table )
    client = bigquery.Client()
    query = ('DELETE FROM `{}.{}.{}` WHERE 1=1'.format(TABLE_NAME,DATASET_ID,TABLE_ID))
    query_job = client.query(query,location='EU')
    query_job.result()
    logger.info('Affected {} rows | Table {}:{}:{} truncated'.format(query_job.num_dml_affected_rows,TABLE_NAME,DATASET_ID,TABLE_ID))

def bq_remove_between(TABLE_NAME, DATASET_ID, TABLE_ID, FROM, TO):
    #Remove existing table ( empty the table )
    client = bigquery.Client()
    query = ('DELETE FROM `{}.{}.{}` WHERE date BETWEEN "{}" AND "{}"'.format(TABLE_NAME,DATASET_ID,TABLE_ID,FROM,TO))
    query_job = client.query(query,location='EU')
    query_job.result()
    logger.info('Affected {} rows | Table {}:{}:{} truncated'.format(query_job.num_dml_affected_rows,TABLE_NAME,DATASET_ID,TABLE_ID))

def bq_remove_custom(TABLE_NAME, DATASET_ID, TABLE_ID, EXTRA):
    #Remove existing table ( empty the table )
    client = bigquery.Client()
    query = ('DELETE FROM `{}.{}.{}` WHERE {}'.format(TABLE_NAME,DATASET_ID,TABLE_ID,EXTRA))
    query_job = client.query(query,location='EU')
    query_job.result()
    logger.info('Affected {} rows | Table {}:{}:{} truncated'.format(query_job.num_dml_affected_rows,TABLE_NAME,DATASET_ID,TABLE_ID))




#Upload data to the BigQuery 
def upload_to_bq(TABLE_NAME, DATASET_ID,TABLE_ID, FILE_NAME):

    logger.info('Start uploading to BigQuery file: {}'.format(FILE_NAME))
    #Big query upload method, full documentation about how to use it,
    #can be found on official google website
    client = bigquery.Client()
 
    dataset_ref = client.dataset(DATASET_ID )
    table_ref = dataset_ref.table(TABLE_ID)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    #job_config.skip_leading_rows = 1
    job_config.autodetect = False

    with open(FILE_NAME, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location='EU',  # Must match the destination dataset location.
            job_config=job_config)  # API request
    
    job.result()  # Waits for table load to complete.
    time.sleep(1)

    logger.info('Loaded {} rows into {}:{}:{}.'.format(job.output_rows,TABLE_NAME,DATASET_ID,TABLE_ID))
    logger.info('Loaded {} rows. | FILE:{}'.format(job.output_rows,FILE_NAME))


def upload_to_bq_csv(TABLE_NAME, DATASET_ID,TABLE_ID, FILE_NAME):
    client = bigquery.Client()
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(TABLE_ID)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = False

    with open(FILE_NAME, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location='EU',  # Must match the destination dataset location.
            job_config=job_config)  # API request

    job.result()  # Waits for table load to complete.
    time.sleep(1)

    logger.info('Loaded {} rows into {}:{}:{}.'.format(job.output_rows,TABLE_NAME,DATASET_ID,TABLE_ID))
    logger.info('Loaded {} rows. | FILE:{}'.format(job.output_rows,FILE_NAME))




#Copy BQ table/query from source to destination
def BQ_TABLE_COPY(SQL_QUERY,PROJECT,DATASET_ID,TABLE,CREATED,WRITE_TRUNCATE):
    #Missing Data = Data which exist in STreamng table and NOT in Order Table
    logger.info('Copying - Started')

    #Set a BigQuery Client libraries
    client = bigquery.Client()

    #Configuration options for query jobs.
    job_config = bigquery.QueryJobConfig()

    #Destination Table - Table where result will be saved to.
    job_config.destination = client.dataset(DATASET_ID).table(TABLE)

    #By using client and job configuration will run the actual job.


    #Optional - Will create table if it not exist, usefull if you testing and have only Streaming table.
    #This is an option will automatically create all tables which needed
    if CREATED == 'CREATE':
        job_config.create_disposition = 'CREATE_IF_NEEDED'
    else:
        logger.info('Auto table creation - Disabled')
    #Truncate the table every time when the data will be written
    if WRITE_TRUNCATE == 'TRUNCATE':
        job_config.write_disposition = 'WRITE_TRUNCATE'
    elif WRITE_TRUNCATE == 'APPEND':
        job_config.write_disposition = 'WRITE_APPEND'
    else: 
        logger.info('Auto table truncation - Disabled')
        
    # Waits for table load to complete.
    wave = client.query(SQL_QUERY,location='EU',job_config=job_config)  
    wave.result()

    # Loggs output
    logger.info("SQL: {}".format(SQL_QUERY))
    logger.info('Copying - Finished')
    logger.info('Loaded {} rows into {}:{}:{}.'.format(wave._query_results.total_rows ,PROJECT,DATASET_ID,TABLE))
    time.sleep(1)
    logger.info('-------------------------------------')




#CSV to GOOGLE STORAGE
def CSV_EXPORT(PROJECT,DATASET_ID,TABLEID,BUCKET_NAME,BUCKET_PATH,FILE):

    logger.error('Start generating files from {} table'.format(TABLEID))

    client = bigquery.Client()

    destination_uri = "gs://{}/{}{}".format(BUCKET_NAME,BUCKET_PATH, "{}.csv".format(FILE))
    dataset_ref = client.dataset(DATASET_ID, project=PROJECT)
    table_ref = dataset_ref.table(TABLEID)

    extract_job = client.extract_table(
            table_ref,
            destination_uri,
            # Location must match that of the source table.
            location="EU",
    )  # API request
    extract_job.result()  # Waits for job to complete.

    logger.info("Bucket:{}, Project:{}, Dataset:{}, Table:{}".format(BUCKET_NAME,PROJECT,DATASET_ID,TABLEID))
    logger.info("Exported {}:{}.{} to {}".format(PROJECT,DATASET_ID,TABLEID, destination_uri))
    time.sleep(1)
    logger.error('-------------------------------------')


#PROJECTS##########################################################################################################

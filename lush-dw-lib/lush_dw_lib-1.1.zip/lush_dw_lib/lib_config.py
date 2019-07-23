import datetime
from datetime import timedelta
import uuid

#BASIC CONFIGURATION
UUID = uuid.uuid4().hex


#LOGGING CONFIGURATION
LOG_FILE = 'LOG.json'
LOG_DATASET_ID = 'social_media'
LOG_TABLE_ID = 'projects_log'

#########################################################################################
#Error handling - Email Configuration                                                   #
#########################################################################################
EMAIL_HOST = "smtp-relay.gmail.com"                                                     #
EMAIL_PORT = 587                                                                        #
EMAIL_SUBJECT = "Python script issue 😱 - Have a look and fix it 🖖"
EMAIL_FROM = "data.services@lush.co.uk"                                                 #
EMAIL_TO = ['denis.sineiko@lush.co.uk'] 
#EMAIL_TO = ['denis.sineiko@lush.co.uk','luke.tomlinson@lush.co.uk','warren@lush.co.uk','simon.chettleburgh@lush.co.uk']
#########################################################################################
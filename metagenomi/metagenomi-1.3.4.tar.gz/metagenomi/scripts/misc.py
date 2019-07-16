from abc import ABCMeta
import json
import pandas as pd
import boto3

from boto3.dynamodb.conditions import Key

from metagenomi.base import MgObj
from metagenomi.logger import logger
from metagenomi.helpers import get_time
from metagenomi.db import batch_client


def write_old_filepath(old, new):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('old-filepaths-map')

    d = {'olds3path': old, 'news3path': new}
    response = table.put_item(Item=d)
    return response

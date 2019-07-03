import os
import sys
from invoke import task
import boto3, botocore
import yaml
import re

BUCKET_ENV_VAR_NAME = 'KVS3_BUCKET'
INIT_FILE = '.kvs3'
DELIM='/'

@task(optional=['bucket'])
def init(ctx, bucket=None):
    """Initialize .kvs3 with name of s3 bucket used as kvs"""
    session = boto3.Session()
    s3 = boto3.client('s3')
    config={}

    if bucket == None and os.environ.get('KVS3_BUCKET') == None:
        bucket_init = input('Enter s3 key value store bucket name: ')
        s3_name_requirements = re.compile("^[a-z0-9]{1}[a-z0-9\-\.]{1,61}[a-z0-9\.]{1}$")
        if s3_name_requirements.match(bucket_init):
            config['bucket'] = bucket_init
            with open(INIT_FILE, 'w') as outfile:
                yaml.dump(config, outfile, default_flow_style=False)
        else:
            print('kvs3: invalid bucket name')
            sys.exit(1)

    validate(s3, bucket)

@task(optional=['bucket'])
def write(ctx, service, key, value, bucket=None):
    """write key/value to kvs"""
    session = boto3.Session()
    s3 = boto3.client('s3')
    bucket = validate(s3, bucket)
    if value == '-':
        value = sys.stdin.buffer.read()
    s3.put_object(
        Bucket=bucket,
        Key=service + DELIM + key,
        Body=value
    )


@task(optional=['bucket'])
def read(ctx, service, key, bucket=None):
    """read key value from kvs"""
    session = boto3.Session()
    s3 = boto3.client('s3')
    bucket = validate(s3, bucket)
    key = service + DELIM + key
    print(get_key(s3, bucket, key))

@task(optional=['bucket'])
def list(ctx, service, bucket=None):
    """list services and keys in kvs"""
    session = boto3.Session()
    s3 = boto3.client('s3')
    if service == 'all':
        service = ''
    else:
        service = service + DELIM
    bucket = validate(s3, bucket)
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=service, Delimiter=DELIM)

    if 'CommonPrefixes' in resp:
        print('All Services')
        for svc in resp['CommonPrefixes']:
            print(svc['Prefix'])

    if 'Contents' in resp:
        col1=max(len(key['Key'].split(DELIM,1)[1]) for key in resp['Contents']) + 5
        print("{:{wid}} {:<5} {}".format('KEY', 'SIZE', 'MODIFIED', wid=col1))
        for key in resp['Contents']:
            print("{:{wid}} {:<5} {:%Y-%m-%d %H:%M:%S}".format(key['Key'].split(DELIM,1)[1], key['Size'], key['LastModified'], wid=col1))


@task(optional=['bucket'])
def setenv(ctx, service, keyfile, bucket=None):
    """retrieve a list of keys from kvs and output in 'export KEY=VALUE' format"""
    session = boto3.Session()
    s3 = boto3.client('s3')
    bucket = validate(s3, bucket)
    if os.path.exists(keyfile):
        with open(keyfile) as infile:
            print(f"# source {service} environment config")
            for line in infile:
                if len(line.split()) > 1:
                    print('kvs3: environment file must contain a single key name per line')
                    sys.exit(1)
                else:
                    key = line.rstrip('\n')
                    value = get_key(s3, bucket, service + DELIM + key)
                    print(f"export {key}=\"{value}\"")
    else:
        print(f"kvs3: file not found - {keyfile}")


def get_key(s3, bucket, key):
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        return resp['Body'].read().decode('utf-8')
    except botocore.exceptions.ClientError as e:
        print(e)

def validate(s3, bucket):
    if bucket == None:
        if os.environ.get('KVS3_BUCKET') == None:
            if os.path.exists(INIT_FILE):
                with open(INIT_FILE, 'r') as infile:
                    data = yaml.load(infile, Loader=yaml.Loader)
                bucket = data['bucket']
            else:
                print('kvs3: use --bucket or $KVS3_BUCKET to set s3 bucket name')
                sys.exit(1)
        else:
            bucket = os.environ.get('KVS3_BUCKET')
    try:
        s3.list_objects(Bucket=bucket)
        return bucket
    except botocore.exceptions.ClientError as e:
        print(f"kvs3: Confirm credentials or bucket name https://{bucket}.s3.amazonaws.com/")
        sys.exit(1)




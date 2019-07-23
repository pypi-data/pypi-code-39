import boto3


def aws_connect(access_key: str, secret_key: str, resource: str = 's3', region: str = 'us-west-2'):
    if access_key and secret_key:
        sess = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        conn = sess.resource(service_name=resource, region_name=region)
    else:
        conn = boto3.resource(service_name=resource, region=region)

    return conn


def s3_upload_file(log, access_key: str, secret_key: str, bucket_name: str, s3_key: str, filepath: str,
                   region: str = 'us-west-2', conn=None):
    if conn:
        s3_connection = conn
    elif access_key and secret_key:
        s3_connection = aws_connect(access_key, secret_key, resource='s3', region=region)
    else:
        s3_connection = aws_connect(None, None, resource='s3', region=region)

    s3_connection.Bucket(bucket_name).upload_file(filepath, s3_key)
    log.info(f'Uploaded {filepath} to s3://{bucket_name}/{s3_key}')

import json
import sys
import boto3
from botocore.exceptions import ClientError
from .config import config

region = config.AWS_REGION


def aws_verify_instance(ip):
    '''
    This function verifies an AWS instance is valid

    :param ip: Private IP Address of AWS instance
    :type ip: unicode
    '''
    client = boto3.client(
        'ec2',
        region_name=region
        )
    try:
        instances = client.describe_instances(
            Filters=[
                {
                    'Name': 'private-ip-address',
                    'Values': [
                        ip,
                        ]
                    },
                ]
            )
        unique = False
        instance = instances['Reservations'][0]['Instances'][0]
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
            if tag['Key'] == 'Unique':
                unique = True
        instance_id = instance['InstanceId']
        instance_state = instance['State']['Name']
        if unique:
            host = ''.join(name.split('.')[:1])
            suffix = '.'.join(ip.split('.')[-1:])
            domain = '.'.join(name.split('.')[1:])
            hostname = host + suffix + '.' + domain
            print(hostname)

            response = {'hostname': hostname,
                        'instance_id': instance_id,
                        'instance_state': instance_state,
                        'unique_name': unique}
        else:
            hostname = name
            print(hostname)
            response = {'hostname': hostname,
                        'instance_id': instance_id,
                        'instance_state': instance_state,
                        }
        return response
    except ClientError as e:
        sys.stderr.write(
            json.dumps(e.response)
            )
        return False


def aws_tag_instance(hostname, instance_id, region):
    client = boto3.client(
        'ec2',
        region_name=region
    )
    client.create_tags(
        Resources=[
            instance_id,
            ],
        Tags=[
            {
                'Key': 'Name',
                'Value': hostname
            },
            {
                'Key': 'Registered',
                'Value': 'True'
            },
        ]
    )

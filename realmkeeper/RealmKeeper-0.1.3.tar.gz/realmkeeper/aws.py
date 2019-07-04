import json
import sys
import logging
import boto3
from botocore.exceptions import ClientError
from .config import config

FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(stream=sys.stdout, level=config.LOG_LEVEL, format=FORMAT)
REGION = config.AWS_REGION


class Instance(object):
    """The Instance object holds EC2 information.

    Args:
        private_ip (unicode str): Private IP Address

    Attributes:
        id (str): EC2 Instance ID
        name (str): EC2 Instance Name Tag
        private_ip (unicode str): EC2 Instance Private IP address
        unique (bool): If set, will require a unique hostname
        state (str): EC2 Instance state (e.g 'running')
        connection(boto3.session.Session.client): Boto3 Connection
    """

    def __init__(self, private_ip):
        self.id = None
        self.name = None
        self.private_ip = private_ip
        self.unique = False
        self.state = None
        self.connection = None

    def connect_ec2(self):
        """Create Boto3 connection."""
        self.connection = boto3.client('ec2', REGION)

    def get_info(self):
        """Get EC2 Instance Metadata."""
        try:
            instance = self.connection.describe_instances(
                Filters=[
                    {
                        'Name': 'private-ip-address',
                        'Values': [
                            self.private_ip,
                            ]
                        },
                    ]
                )['Reservations'][0]['Instances'][0]

            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
                if tag['Key'] == 'Unique':
                    self.unique = True
            self.id = instance['InstanceId']
            self.state = instance['State']['Name']
            if self.unique:
                host = ''.join(name.split('.')[:1])
                suffix = '.'.join(self.private_ip.split('.')[-1:])
                domain = '.'.join(name.split('.')[1:])
                hostname = host + suffix + '.' + domain
                self.name = hostname
            else:
                self.name = name
        except ClientError as e:
            logging.error(e.response)
        except IndexError as i:
            logging.info(
                'EC2 Instance with private IP {} not found'.format(self.private_ip))

        def set_tags(self):
            """Set EC2 Instance tags."""
            self.connection.create_tags(
                Resources=[
                    self.id,
                    ],
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': self.name
                        },
                    {
                        'Key': 'Registered',
                        'Value': 'True'
                        },
                    ]
                )

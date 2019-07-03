#!/usr/bin/env python
from __future__ import print_function
from ec2_metadata import ec2_metadata

import argparse
import sys
import os
import boto3
import uuid
import time
import json
from tabulate import tabulate

#print (ec2_metadata.private_hostname)
#print (ec2_metadata.private_ipv4)


class NodeRegister(object):

    def __init__(self, ddb_table, region_name):
        self.ddb_resource = boto3.resource('dynamodb', region_name=region_name)
        self.ddb_region = region_name
        try:
            self.ddb_table = self.ddb_resource.Table(ddb_table)
        except Exception as _error:
            print(_error)

    def register(self, hostname, private_ip):
        print('Registering Node => {}'.format(hostname))
        time_stamp = time.asctime( time.localtime(time.time()) )
        self.ddb_table.put_item(
            Item={
                'hostname': hostname,
                'private-ip': private_ip,
                'node-type': 'unassigned',
                'node-state': 'running',
                'timestamp': time_stamp
            }
        )

    # Assign a role to exisitng record
    def assign_role(self,table_name, hostname, private_ip, role):
        ddb_resource = boto3.resource('dynamodb', region_name=self.ddb_region)
        time_stamp = time.asctime( time.localtime(time.time()) )
        
        try:
            table = ddb_resource.Table(table_name)
            # Load Host data
            response = table.get_item(Key={'hostname': hostname})
            item = response['Item']
            # Load new Host data 
            item['node-type'] = role
            item['timestamp'] = time_stamp
            # Update Host data 
            table.put_item(Item=item)
        except Exception as _error:
            print(_error)
    
    # Assign a set-state to exisitng record
    def set_state(self,table_name, hostname, state):
        ddb_resource = boto3.resource('dynamodb', region_name=self.ddb_region)
        time_stamp = time.asctime( time.localtime(time.time()) )
    
        try:
            table = ddb_resource.Table(table_name)
            # Load Host data
            response = table.get_item(Key={'hostname': hostname})
            item = response['Item']
            # Load new Host data 
            item['node-state'] = state
            item['timestamp'] = time_stamp
            # Update Host data 
            table.put_item(Item=item)
        except Exception as _error:
            print(_error)    

    def db_list(self, table_name):
        ddb_resource = boto3.resource('dynamodb', region_name=self.ddb_region)
        try:
            table = ddb_resource.Table(table_name)

            response = table.scan()
            registered = response['Items']

            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                registered.extend(response['Items'])

            print ('{:<32}{:<15}{:<15}{:<15}{:<45}'.format(
                                               'HOSTNAME',
                                               'NODE_TYPE',
                                               'NODE_STATE',
                                               'PRIVATE_IP',
                                               'TIME_STAMP',
                                               ))
            for host in registered:
                print ('{:<32}{:<15}{:<15}{:<15}{:<45}'.format(
                                                   host['hostname'],
                                                   host['node-type'],
                                                   host['node-state'],
                                                   host['private-ip'],
                                                   host['timestamp'],
                                                   ))
            
        except Exception as _error:
            print(_error)
                    
def db_create_standalone(table_name, region_name):

    ddb_resource = boto3.resource('dynamodb', region_name=ec2_metadata.region)
    try:
        table = ddb_resource.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'hostname',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'hostname',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )
        print('Creating ...... Table ->[{}]'.format(table_name))
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        return table
    except Exception as table_exists:
        if table_exists:
            print('Using Existing Table...... ->[{}]'.format(table_name))
            table = ddb_resource.Table(table_name)
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            return table


def is_ec2():
    try:
        if ec2_metadata.instance_id:
            return True
    except Exception:
       return False

def is_register(ddb_table):
    dynamodb = boto3.client('dynamodb', region_name=ec2_metadata.region)
    existing_tables = dynamodb.list_tables()
    if ddb_table in existing_tables['TableNames']:
        #print(existing_tables['TableNames'])
        return True
    else:
        print('Table {} does not exist in the specified region'.format(ddb_table))
        return False

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--create_ddb", help="Create a new DynamoDB table", action='store_true')
action_createdb = parser.add_argument_group('actions')
action_group = action_createdb.add_mutually_exclusive_group()
action_group.add_argument("-a", "--assign", help="Set the node type of an existing node")
action_group.add_argument("-s", "--set_state", help="Set the node state of an existing node (running|terminated)")
action_group.add_argument("-r", "--register_node", help="Add a new node to the DynamoDB table", action='store_true')
action_group.add_argument("-l", "--list", help="List Registered Node in given DynamoDB Table", action='store_true')
required_group = parser.add_argument_group('required', 'for (assign|state|list|register_node) actions')
required_group.add_argument("-D", "--dynamodb_table", help="Name of Existing DynamoDB")
args = parser.parse_args()


def main():
    ddb = None

    if args.create_ddb:
        if len(sys.argv) <= 2:
            if not is_ec2():
                print('This utility is only supported on AWS ec2')
            else:
                ddb='noderegister-{}'.format(str(uuid.uuid4()))
                db_create_standalone(ddb, ec2_metadata.region)
                print ('Pass the -D flag to use this DynamoDBTable \n\t EXAMPLE: {} -D {}'.format(os.path.basename(__file__), ddb))
                sys.exit(0)
        else:
            print ('Too many args --create_ddb does not require a value \n\t EXAMPLE: {} -c'.format(os.path.basename(__file__)))
            sys.exit(1)

    elif args.list:
        if args.dynamodb_table:
            if is_register(args.dynamodb_table):
                new_register = NodeRegister(args.dynamodb_table, ec2_metadata.region)
                new_register.db_list(args.dynamodb_table)
                sys.exit(0)
        else:
            print('Node register not found! --list operation requires you to pass in an existing DynamoDB')
            print('EXAMPLE: \n\t{} -D Existing-DynamoDb-Name -l {}'.format(os.path.basename(__file__), ddb))

    elif args.assign:
        if args.dynamodb_table:
            if is_register(args.dynamodb_table):
                new_register = NodeRegister(args.dynamodb_table, ec2_metadata.region)
                new_register.assign_role(args.dynamodb_table, ec2_metadata.private_hostname, ec2_metadata.private_ipv4, args.assign)
        else:
            print('Node register not found! --assign operation requires you to pass in an existing DynamoDB')
            print('EXAMPLE: \n\t{} -D Existing-DynamoDb-Name -a {}'.format( os.path.basename(__file__), ddb))

    elif args.set_state:
        if args.dynamodb_table:
            if is_register(args.dynamodb_table):
                new_register = NodeRegister(args.dynamodb_table, ec2_metadata.region)
                new_register.set_state(args.dynamodb_table, ec2_metadata.private_hostname, args.set_state)
        else:
            print('Node register not found! --set_state operation requires you to pass in an existing DynamoDB')
            print('EXAMPLE: \n\t{} -D Existing-DynamoDb-Name -s {}'.format( os.path.basename(__file__), ddb))

    elif args.register_node:
        if args.dynamodb_table:
            if is_register(args.dynamodb_table):
                #Create Node Register Table
                if not is_ec2():
                    print('This utility is only supported on AWS ec2')
                else:
                    new_register = NodeRegister(args.dynamodb_table, ec2_metadata.region)
                    new_register.register(ec2_metadata.private_hostname,ec2_metadata.private_ipv4)
        else:
            print('Node register not found! --regiser_node operation requires you to pass in an existing DynamoDB')
            print('EXAMPLE: \n\t{} -D Existing-DynamoDb-Name -r {}'.format( os.path.basename(__file__), ddb))
    else:
        parser.print_help()

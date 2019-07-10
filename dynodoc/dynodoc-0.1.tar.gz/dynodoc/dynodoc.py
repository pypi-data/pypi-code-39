import base64
import json

import click
import boto3
from botocore.exceptions import ClientError

class JsonLoaded(click.ParamType):
    name = "map"
    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except TypeError:
            self.fail(
                "invalid json",
                param,
                ctx,
            )
        except ValueError:
            self.fail("invalid json", param, ctx)


class Config(object):
    
    def __init__(self):
        pass
        
config = click.make_pass_decorator(Config, ensure=True)

def name_has_value(name):
    if not name:
        click.echo('Tables need names')
        return False
    else:
        return True 

def more_than_one(first, second, third):
        if (first and (second or third)) or (second and (third or first)) or (third and (first or second)):
            return True

def string_to_correct_number(str_num):
    if '.' in str_num:
        num = float(str_num)
        return num
    else:
        num = int(str_num)
        return num

def str_to_b64(str):
    return base64.b64encode(bytes(str,'utf-8'))

def table_caller(f, **kwargs):
    values = {}
    for k in kwargs:
        if kwargs[k] is not None:
            values[k] = kwargs[k]
    return f(**values)


## Start of Decorators
def hash_and_sort_keys(function):
    function = click.option('-sh', '--str-hash', nargs=2, type=str, help='Name of the string hash key and the value')(function)
    function = click.option('-nh', '--num-hash', nargs=2, type=str, help='Name of the number hash key and the value')(function)
    function = click.option('-bh', '--bin-hash', nargs=2, type=str, help='Name of the binary hash key and the value')(function)
    function = click.option('-ss', '--str-sort', nargs=2, type=str, help='Name of the string sort key and the value')(function)
    function = click.option('-ns', '--num-sort', nargs=2, type=str, help='Name of the number sort key and the value')(function)
    function = click.option('-bs', '--bin-sort', nargs=2, type=str, help='Name of the binary sort key and the value')(function)
    return function

def hash_and_sort_key_names(function):
    function = click.option('-sh', '--str-hash', type=str, help='Name of the string hash key')(function)
    function = click.option('-nh', '--num-hash', type=str, help='Name of the number hash key')(function)
    function = click.option('-bh', '--bin-hash', type=str, help='Name of the binary hash key')(function)
    function = click.option('-ss', '--str-sort', type=str, help='Name of the string sort key')(function)
    function = click.option('-ns', '--num-sort', type=str, help='Name of the number sort key')(function)
    function = click.option('-bs', '--bin-sort', type=str, help='Name of the binary sort key')(function)
    return function

def name(function):
    function = click.option('--name', type=str, required=True, help='Name of the table')(function)
    return function

def capacity(function):
    function = click.option('--show-capacity', type=click.Choice(['INDEX', 'TOTAL', 'NONE']), help='Return consumed capacity for the request')(function)
    return function
    
def reader(function):
    function = click.option('--consistent', is_flag=True, help='Enable ConsistentRead')(function)
    return function

def attribute_names(function):
    function = click.option('--expression-attribute-names', type=JsonLoaded(), help='One or more substitution tokens for attribute names in an expression')(function)
    return function

def attribute_values(function):
    function = click.option('--expression-attribute-values', type=JsonLoaded(), help='One or more values that can be substituted in an expression')(function)
    return function

def condition_expression(function):
    function = click.option('--condition-expression', type=str, help='A condition that must be satisfied in order for a conditional PutItem operation to succeed')(function)
    return function

def update_expression(function):
    function = click.option('--update-expression', type=str, help='An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them')(function)
    return function

def full_response(function):
    function = click.option('--full-response', is_flag=True, help='Returns  full http resonse')(function)
    return function

def project(function):
    function = click.option('--project', type=str, help='Projection expression to use')(function)
    return function

def return_vals(function):
    function = click.option('--return_vals', type=click.Choice(['NONE', 'ALL_OLD']), help='Attributes to return after succesful put')(function)
    return function

def update_return_vals(function):
    function = click.option('--update_return_vals', type=click.Choice(['NONE', 'ALL_OLD', 'UPDATED_OLD', 'ALL_NEW', 'UPDATED_NEW']), help='Attributes to return after succesful put')(function)
    return function

def item_collection_metrics(function):
    function = click.option('--item_collection_metrics', type=click.Choice(['NONE', 'SIZE']), help='Whether item collection metrics are returned')(function)
    return function

def item(function):
    function = click.option('--item', type=JsonLoaded(), required=True, help='Item to put into table')(function)
    return function

def query_and_scan(function):
    function = click.option('--start-key', type=JsonLoaded(), help='The primary key of the first item that this operation will evaluate')(function)
    function = click.option('--index-name', type=str, help='name of an index to query')(function)
    function = click.option('--select', type=click.Choice(['ALL_ATTRIBUTES', 'ALL_PROJECTED_ATTRIBUTES', 'SPECIFIC_ATTRIBUTES', 'COUNT']), help='the attributes to be returned in the result')(function)
    function = click.option('--filter-expression', type=str, help='the condition that specifies the key values for items to be retrieved by the Query action')(function)
    function = click.option('--limit', type=int, help='the maximum number of items to evaluate (not necessarily the number of matching items')(function)
    return function
## End of Decorators

@click.group()
@click.pass_context
def cli(config):
    '''
    DynamoDB CLI tool that uses the document interface. With a document interface, you do not need to specify Data Type Descriptors; the data types are implied by the semantics of the data itself.
    '''

@cli.command()
@click.pass_context
@name
@hash_and_sort_key_names
def create_table(config, name, str_hash, num_hash, bin_hash, str_sort, num_sort, bin_sort):
    '''
    Adds a new table to your account
    '''

    #only one hash key must be given
    if more_than_one(str_hash, bin_hash, num_hash):
        click.echo('Tables can only have a single hash key')
        return

    #there's atleast one hash key given
    if not (str_hash or bin_hash or num_hash):
        click.echo('Tables need atleast one hash key')
        return
    
    attribute_definitions = []
    def AttributeDefiner(attr_name, attr_type):
        attribute_definitions.append({'AttributeName': attr_name, 'AttributeType': attr_type})

    if str_hash:
        AttributeDefiner(str_hash, 'S')
    elif bin_hash:
        AttributeDefiner(bin_hash, 'B')
    else:
        AttributeDefiner(num_hash, 'N')
    
    hash_key_name = str_hash or bin_hash or num_hash
    key_schema = []
    key_schema.append({
            'AttributeName': hash_key_name,
            'KeyType': 'HASH'
        })

    #Check if there's any and only one sort key, and if so, append it to AttributeDefinitions argument and the key_schema argument

    #if given, only one sort key must be given
    if more_than_one(str_sort, bin_sort, num_sort):
        click.echo('Tables can only have a single sort key')
        return

    if str_sort or bin_sort or num_sort:
        if str_sort:
            AttributeDefiner(str_sort, 'S')
        elif bin_sort:
            AttributeDefiner(bin_sort, 'B')
        else:
            AttributeDefiner(num_sort, 'N')
        sort_key_name = str_sort or bin_sort or num_sort
        key_schema.append({
                'AttributeName': sort_key_name,
                'KeyType': 'RANGE'
            })
    
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.create_table(
            AttributeDefinitions=attribute_definitions,
            TableName=name,
            KeySchema=key_schema,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        click.echo(table.table_name)
        click.echo(table.key_schema)
        click.echo(table.attribute_definitions)
        click.echo(table.provisioned_throughput)
    except ParamValidationError as e:
        click.echo(e)

@cli.command()
@click.pass_context
@hash_and_sort_keys
@name
@capacity
@attribute_names
@full_response
@reader
@project
def get_item(config, name, str_hash, num_hash, bin_hash, str_sort, num_sort, bin_sort, full_response, consistent, show_capacity, project, expression_attribute_names):
    '''
    Returns a set of attributes for the item with the given PK
    '''
    #only one hash key must be given
    if more_than_one(str_hash, bin_hash, num_hash):
        click.echo('Tables can only have a single hash key')
        return

    #there's atleast one hash key given
    if not (str_hash or bin_hash or num_hash):
        click.echo('Tables need atleast one hash key')
        return
    
    key = {}    

    if str_hash:
        key[str_hash[0]] = str_hash[1]
    elif bin_hash:
        key[bin_hash[0]] =  str_to_b64(bin_hash[1])
    else:
        try:
            key[num_hash[0]] = string_to_correct_number(num_hash[1])
        except ValueError:
            click.echo('Not a valid hash key number')
            config.abort()
    
    #check and get sort key
    if more_than_one(str_sort, bin_sort, num_sort):
        click.echo('Tables can only have a single sort key')
        return
    
    if str_sort:
        key[str_sort[0]] = str_sort[1]
    elif bin_sort:
        key[bin_sort[0]] =  str_to_b64(bin_sort[1])
    elif num_sort:
        try:
            key[num_sort[0]] = string_to_correct_number(num_sort[1])
        except ValueError:
            click.echo('Not a valid sort key number')
            config.abort()
    
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(name)

        response = table_caller(table.get_item, 
            Key=key,
            ConsistentRead=consistent,
            ReturnConsumedCapacity=show_capacity,
            ProjectionExpression=project,
            ExpressionAttributeNames=expression_attribute_names)
        
        click.echo(response if full_response else response['Item'])
    except ClientError as e:
        click.echo(e)


@cli.command()
@click.pass_context
@name
@capacity
@attribute_names
@attribute_values
@condition_expression
@full_response
@item
@return_vals
def put_item(config, name, item, return_vals, show_capacity, condition_expression, expression_attribute_names, expression_attribute_values, full_response):
    '''
    Creates a new item, or replaces an old item with a new item
    '''
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(name)
        response = table_caller(table.put_item, 
            Item=item, 
            ReturnValues=return_vals,
            ReturnConsumedCapacity=show_capacity,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values)
        
        if full_response:
            click.echo(response)
        else:
            if show_capacity and ('ConsumedCapacity' in response.keys()):
                click.echo(response['ConsumedCapacity'])
            if return_vals == 'ALL_OLD':
                click.echo(response['Attributes'])
        #click.echo(response if full_response or show_capacity else (response['Attributes'] if return_vals == 'ALL_OLD' else None))
    except ClientError as e:
        click.echo(e)

    
      
@cli.command()
@name
@capacity
@query_and_scan
@attribute_names
@attribute_values
@reader
@project
@click.option('--scan-reverse', is_flag=True, type=bool, help='Reads the results in reverse order by sort key value')
@click.option('--key-condition-expression', type=str, required=True, help='The condition that specifies the key values for items to be retrieved by the Query action')
@full_response
@click.pass_context
def query(config, name, index_name, project, key_condition_expression, filter_expression, expression_attribute_names, expression_attribute_values, select, show_capacity, start_key, scan_reverse, full_response, limit, consistent):
    '''
    Finds items based on primary key values. 
    '''
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(name)
        response = table_caller(table.query, 
            ReturnConsumedCapacity=show_capacity,
            Select=select,
            ProjectionExpression=project,
            ExclusiveStartKey=start_key,
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            FilterExpression=filter_expression,
            ScanIndexForward=scan_reverse,
            Limit=limit,
            ConsistentRead=consistent)
        click.echo(response if full_response or show_capacity else response['Items'])
    except ClientError as e:
        click.echo(e)


@cli.command()
@name
@capacity
@query_and_scan
@attribute_names
@attribute_values
@reader
@project
@full_response
@click.option('--total-segments', type=int, help='For parallel scans, total-segments represents the total number of segments into which the scan operation will be divided')
@click.option('--segment', type=int, help='For parallel scans, segment identifies an individual segment to be scanned by an application worker')
@click.pass_context
def scan(config, name, index_name, project, filter_expression, expression_attribute_names, expression_attribute_values, select, show_capacity, start_key, full_response, limit, consistent, total_segments, segment):
    '''
    Returns item(s) by accessing every item in a table or index
    '''
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(name)
        response = table_caller(table.scan, 
            ReturnConsumedCapacity=show_capacity,
            Select=select,
            ProjectionExpression=project,
            ExclusiveStartKey=start_key,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            FilterExpression=filter_expression,
            TotalSegments=total_segments,
            Segment=segment,
            Limit=limit,
            ConsistentRead=consistent)
        click.echo(response if full_response or show_capacity else response['Items'])
    except ClientError as e:
        click.echo(e)

@cli.command()
@name
@capacity
@full_response
@hash_and_sort_keys
@return_vals
@item_collection_metrics
@condition_expression
@attribute_names
@attribute_values
@click.pass_context
def delete_item(config, name, str_hash, num_hash, bin_hash, str_sort, num_sort, bin_sort, show_capacity, full_response, return_vals, item_collection_metrics, condition_expression, expression_attribute_names, expression_attribute_values):
    '''
    Deletes a single item in a table by primary key
    '''
    #only one hash key must be given
    if more_than_one(str_hash, bin_hash, num_hash):
        click.echo('Tables can only have a single hash key')
        return

    #there's atleast one hash key given
    if not (str_hash or bin_hash or num_hash):
        click.echo('Tables need atleast one hash key')
        return
    
    key = {}    

    if str_hash:
        key[str_hash[0]] = str_hash[1]
    elif bin_hash:
        key[bin_hash[0]] =  str_to_b64(bin_hash[1])
    else:
        try:
            key[num_hash[0]] = string_to_correct_number(num_hash[1])
        except ValueError:
            click.echo('Not a valid hash key number')
            config.abort()
    
    #check and get sort key
    if more_than_one(str_sort, bin_sort, num_sort):
        click.echo('Tables can only have a single sort key')
        return
    
    if str_sort:
        key[str_sort[0]] = str_sort[1]
    elif bin_sort:
        key[bin_sort[0]] =  str_to_b64(bin_sort[1])
    elif num_sort:
        try:
            key[num_sort[0]] = string_to_correct_number(num_sort[1])
        except ValueError:
            click.echo('Not a valid sort key number')
            config.abort()
    
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(name)

        response = table_caller(table.delete_item, 
            Key=key,
            ReturnValues=return_vals,
            ReturnItemCollectionMetrics=item_collection_metrics,
            ReturnConsumedCapacity=show_capacity,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values)
        
        if full_response:
            click.echo(response)
        else:
            if item_collection_metrics and ('ItemCollectionMetrics' in response.keys()):
                click.echo(response['ItemCollectionMetrics'])
            if return_vals and ('Attributes' in response.keys()):
                click.echo(response['Attributes'])
    except ClientError as e:
        click.echo(e)

@cli.command()
@click.pass_context
@name
@update_return_vals
@item_collection_metrics
@capacity
@hash_and_sort_keys
@condition_expression
@update_expression
@attribute_names
@attribute_values
def update_item(config, name, str_hash, num_hash, bin_hash, str_sort, num_sort, bin_sort, update_return_vals, show_capacity, item_collection_metrics, condition_expression, update_expression, expression_attribute_names, expression_attribute_values):
    '''
    Edits an existing item's attributes, or adds a new item to the table if it does not already exist
    '''
    #only one hash key must be given
    if more_than_one(str_hash, bin_hash, num_hash):
        click.echo('Tables can only have a single hash key')
        return

    #there's atleast one hash key given
    if not (str_hash or bin_hash or num_hash):
        click.echo('Tables need atleast one hash key')
        return
    
    key = {}    

    if str_hash:
        key[str_hash[0]] = str_hash[1]
    elif bin_hash:
        key[bin_hash[0]] =  str_to_b64(bin_hash[1])
    else:
        try:
            key[num_hash[0]] = string_to_correct_number(num_hash[1])
        except ValueError:
            click.echo('Not a valid hash key number')
            config.abort()
    
    #check and get sort key
    if more_than_one(str_sort, bin_sort, num_sort):
        click.echo('Tables can only have a single sort key')
        return
    
    if str_sort:
        key[str_sort[0]] = str_sort[1]
    elif bin_sort:
        key[bin_sort[0]] =  str_to_b64(bin_sort[1])
    elif num_sort:
        try:
            key[num_sort[0]] = string_to_correct_number(num_sort[1])
        except ValueError:
            click.echo('Not a valid sort key number')
            config.abort()
    
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(name)

        response = table_caller(table.update_item, 
            Key=key,
            ReturnValues=update_return_vals,
            ReturnItemCollectionMetrics=item_collection_metrics,
            ReturnConsumedCapacity=show_capacity,
            ConditionExpression=condition_expression,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values)
        
        if full_response:
            click.echo(response)
        else:
            if item_collection_metrics and ('ItemCollectionMetrics' in response.keys()):
                click.echo(response['ItemCollectionMetrics'])
            if return_vals and ('Attributes' in response.keys()):
                click.echo(response['Attributes'])
    except ClientError as e:
        click.echo(e)

from os import path
from json import loads
from configparser import ConfigParser
import requests
import click
from requests.auth import HTTPBasicAuth
from PyInquirer import prompt, print_json

from jarvis.utils import check_folder_and_files
from jarvis.constants import openproject_config_file, statuses

parser = ConfigParser(allow_no_value=True)

@click.group()
def main():
   pass


@main.command()
#@click.option('status', '-s', required=True, type=click.Choice(['work', 'close', 'hold','pass','fail','testing','done', 'new']))
#@click.option('task_id', '-i', required=True, type=int)
@click.argument('status',type=click.Choice(['work', 'close', 'hold','pass','fail','testing','done', 'new']))
@click.argument('task_id',type=int)
def task(status,task_id):
  """
    Update a specific task that you have access to 
  """
  # Retrive The API Key And Base URL
  # Read The OpenProject Config File
  parser.read(openproject_config_file)
 
  if(parser.has_option('config','base_url') and parser.has_option('config','api_key')):
    base_url = parser.get('config','base_url')
    api_key = parser.get('config','api_key')
  else:
    click.echo('Please Run `jarvis configure` First')
    return 0
  
  workpackage_url = base_url + '/api/v3/work_packages/' + str(task_id)
  # Request For Workpackage
  resp = requests.get(workpackage_url,auth=HTTPBasicAuth('apikey', api_key))
  json_resp = loads(resp.text)

  lockVersion = json_resp['lockVersion']
  for s in statuses:
    if(status == s['status']):
       update_status = s['_links']
  payload = {
  "lockVersion": lockVersion,
  "_links":
      update_status
  }

  # Update Workpackages
  update_resp = requests.patch(workpackage_url, json=payload, 
  headers={
    "Content-Type": "application/json"
  },
  auth=HTTPBasicAuth('apikey', api_key))
  updated_json_resp = loads(update_resp.text)
  task = loads(resp.text)
  click.echo(str(task['id']) + '\t' + task['_links']['status']['title'] + '\t' + task['subject'])

@main.command()
def tasks():
  """
    Retrives a list of tasks your tasks from OpenProject
  """
  # Retrive The API Key And Base URL
  # Read The OpenProject Config File
  parser.read(openproject_config_file)
 
  if(parser.has_option('config','base_url') and parser.has_option('config','api_key')):
    base_url = parser.get('config','base_url')
    api_key = parser.get('config','api_key')
  else:
    click.echo('Please Run `jarvis configure` First')
    return 0

  # Request For Workpackage
  resp = requests.get(base_url + '/api/v3/work_packages?pageSize=25&filters=[{ "assigneeOrGroup": { "operator": "=", "values": "me" }}]&sortBy=[["id", "asc"]]',auth=HTTPBasicAuth('apikey', api_key))
  json_resp = loads(resp.text)
  raw_tasks = json_resp['_embedded']['elements']

  # Display Workpackages
  for task in raw_tasks:
    if(task['_links']['status']['title'] != 'Closed'):
      click.echo(str(task['id']) + '\t' + task['_links']['status']['title'] + '\t' + task['subject'] + '\t' 
        + base_url + '/work_packages/' + str(task['id']))

@main.command()
def configure():
  """
    Helps you manage the Open Project Config
  """
  # Read The OpenProject Config File
  parser.read(openproject_config_file)
  
  # Check If Config Section Exits Else Create
  if(parser.has_section('config')):
      config_section = parser['config']
  else:
    parser.add_section('config')
    config_section = parser['config']
  
  # Questions For Base URL & API Key
  questions = [
  {
    'type': 'input',
    'name': 'base_url',
    'message': 'Open Project Base URL',
    'default': config_section.get('base_url','')
  },
  {
    'type': 'input',
    'name': 'api_key',
    'message': 'Your Open Project API Key',
    'default': config_section.get('api_key','')
  },
  ]

  # Prompting For User Inputs
  answers = prompt(questions)
  
  # Extracting The Data From Answers To Save In ConfigParser
  parser.set('config','base_url', answers['base_url'])
  parser.set('config','api_key', answers['api_key'])
  
  # Saving The Config
  with open(openproject_config_file, 'w') as configfile:
    parser.write(configfile)

if __name__ == '__main__':
    check_folder_and_files()
    main()

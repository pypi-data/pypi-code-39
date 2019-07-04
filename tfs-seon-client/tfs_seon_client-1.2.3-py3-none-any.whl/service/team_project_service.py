import pika
import uuid
import os
import json
from pprint import pprint
from .abstract_service import Abstract_Service

class Team_Project_Service (Abstract_Service):
    
    def __init__(self):
        Abstract_Service.__init__(self,'integration.tfs.team_project') 
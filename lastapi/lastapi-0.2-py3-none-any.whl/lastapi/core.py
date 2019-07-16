import yaml
import requests
import re
import os, sys

from types import SimpleNamespace
from pykwalify.core import Core

class MySimpleNamespace(SimpleNamespace):
  def dict(self):
    return self.__dict__

def determine_path():
  """Borrowed from wxglade.py"""
  try:
    root = __file__
    if os.path.islink(root):
        root = os.path.realpath(root)
    return os.path.dirname(os.path.abspath (root))
  except:
    print( "I'm sorry, but something is wrong.")
    print( "There is no __file__ variable. Please contact the author.")
    sys.exit()

GLOBAL_PARAMETER_PATTERN = re.compile('(\$\{([^\}]+)\})')
# schema is a dict object reading from yaml
def traverse_schema(schema, pattern, params={}):
  if isinstance(schema, dict):
    processed_schema = {}
    for key, value in schema.items():
      processed_schema[key] = traverse_schema(value, pattern, params)
    return MySimpleNamespace(**processed_schema)

  elif isinstance(schema, list):
    return [ traverse_schema(v, pattern, params) for v in schema ]
  elif isinstance(schema, str):
    return process_parameters(schema, pattern, params)
  else:
    return schema

def process_parameters(template, compiled_pattern, params):
  found = compiled_pattern.search(template)
  if found:
    return replace_argument(template, found).format(**params)
  else:
    return template

def replace_argument(template, match):
  groups = match.groups()
  search = groups[0]
  if len(groups) > 1:
    replace = groups[1]
  else:
    replace = groups[0]
  return template.replace(search, "{{{0}}}".format(replace))

class LastApi:
  def __init__(self, api_name):
    api_definition_file = "{0}.yaml".format(api_name)
    api_parameters_file = "{0}-params.yaml".format(api_name)
    c = Core(source_file=api_definition_file, schema_files=[determine_path() + "/schemas/schema.yaml"])
    c.validate(raise_exception=True)
    with open(api_parameters_file, 'r') as fp:
      params = yaml.load(fp)
    with open(api_definition_file, 'r') as fp:
      self.schema = yaml.load(fp)
    self.headers = traverse_schema(self.schema['Headers'], GLOBAL_PARAMETER_PATTERN, params)
    self.base = traverse_schema(self.schema['Base'], GLOBAL_PARAMETER_PATTERN, params)

  def invoke_api(self, action_name, params):
    action = traverse_schema(self.schema['Actions'][action_name], GLOBAL_PARAMETER_PATTERN, params)
    if self.headers.dict()['Content-Type'] == 'application/json':
      response = requests.request(
        method=action.Method,
        url="{0}://{1}{2}".format(self.base.Protocol, self.base.Host, ''.join(action.Path)),
        headers=self.headers.dict(),
        json=action.Payload.dict()
      )
    else:
      response = requests.request(
        method=action.Method,
        url="{0}://{1}{2}".format(self.base.Protocol, self.base.Host, ''.join(action.Path)),
        headers=self.headers.dict(),
        data=action.Payload.dict()
      )
    return response
"""
  curl -X PUT $CFAPI/zones/$1/dns_records/$2 \
    -H "X-Auth-Key: $CFKEY" \
    -H "X-Auth-Email: raynix@gmail.com" \
    -H "Content-type: application/json" \
    --data "{\"type\":\"$3\",\"name\":\"$4\",\"content\":\"$5\",\"ttl\":1,\"proxied\":true}"
"""

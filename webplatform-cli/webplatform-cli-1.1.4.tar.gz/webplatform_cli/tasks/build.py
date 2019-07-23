from docker import APIClient
import os

client = APIClient(base_url="unix://var/run/docker.sock")

def run(service, path, context=None, force=False):
   image_name = 'webplatform-base:latest'

   # dockerfile = path + 'Dockerfile'
   if not context:
      context = path

   print(path, context)
   print("Building base image.")
   kwargs = {
      'nocache': force,
      'decode': True,
      'forcerm': True,
      'path': context,
      'dockerfile': open(path),
      'rm': True,
      'tag': image_name,
      # 'container_limits': {
      #    'cpusetcpus': '0-4',
      #    'memory': 1073741824,
      # }
   }
   for line in client.build(**kwargs):
      if "stream" in line: print(line['stream'])
   print("Done -- building base image.")

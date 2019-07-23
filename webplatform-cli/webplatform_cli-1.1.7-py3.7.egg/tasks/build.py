from docker import APIClient
import os

client = APIClient(base_url="unix://var/run/docker.sock")

def run(service, path, force=False):
   image_name = 'webplatform-base:latest'

   print("Building base image.")
   kwargs = {
      'nocache': force,
      'decode': True,
      'forcerm': True,
      'path': path,
      'dockerfile': path + "/Dockerfile",
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

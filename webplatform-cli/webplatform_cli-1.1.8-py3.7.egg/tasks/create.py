from ..containers import main
import json


def container(client, network, service):
   base_path = main.base_path
   settings = main.settings.get_config(service)

   name = "webplatform-%s" % service
   num_cores = main.settings.get_num_cores(service, get_range=True)

   environment = main.get_environment(service)

   volumes = {
      "%s/docker/actions/%s" % (base_path, service): {
         "bind": "/home/container/actions",
         "mode": "rw",
      },
      "%s/data/%s" % (base_path, service): {
         "bind": "/home/container/data",
         "mode": "rw",
      },
      "%s/docker/%s" % (base_path, service): {
         "bind": "/home/container/config",
         "mode": "rw",
      },
   }

   if "volumes" in settings['container']:
      for key, path in settings['container']['volumes'].items():
         volumes[path] = {
            "bind": "/home/container/%s" % key,
            "mode": "rw"
         }

   volumes = main.add_volumes(volumes)

   kwargs = {
      **settings['container'],
      "image": "webplatform-base:latest",
      "hostname": service,
      "tty": True,
      "environment": environment,
      "name": name,
      "volumes": volumes,
      "command": "/home/container/actions/entry.sh",
   }

   if num_cores != None:
      kwargs['cpuset_cpus'] = num_cores

   container = client.containers.create(**kwargs)
   network.connect(container, aliases=[service])

   return container
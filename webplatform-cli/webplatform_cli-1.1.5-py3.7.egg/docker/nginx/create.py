from containers import main

base_path = main.base_path
instance = main.instance
volumes = main.volumes

service = "nginx"
service_name = service

settings = main.settings.get_config(service)

name = "cee-tools-%s-%s" % (instance, service_name)
num_cores = main.settings.get_num_cores(service, get_range=True)

environment = main.get_environment(service)

def create(client, network):
   devel_volumes = {
      base_path + "/frontend/dist/": {
         "bind": "/home/cee-tools/frontend/",
         "mode": "rw",
      },
      "%s/setup/logs/%s/%s/" % (base_path, instance, service): {
         "bind": "/home/cee-tools/logs/",
         "mode": "rw",
      },
      "%s/setup/instances/%s/%s/config/" % (base_path, instance, service): {
         "bind": "/home/container/config/",
         "mode": "rw",
      },
      "%s/setup/instances/common/%s/actions/" % (base_path, service): {
         "bind": "/home/container/actions/",
         "mode": "rw",
      },
   }
   volumes = main.add_volumes(devel_volumes)
   ports = {
      str(settings['port-https']): settings['port-https'],
   }

   kwargs = {
      "image": "cee-tools-%s-%s:latest" % (instance, service),
      "name": name,
      "hostname": service,
      "tty": True,
      "ports": ports,
      "mem_limit": "4g",
      "environment": environment,
      "volumes": volumes,
   }

   if num_cores != None:
      kwargs['cpuset_cpus'] = num_cores

   container = client.containers.create(**kwargs)
   network.connect(container, aliases=[service])
   return container

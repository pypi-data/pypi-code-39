#!/bin/python3

import os
import sys
import time
import subprocess
from subprocess import call


def _print(msg, index=1):
    os.system('echo "\n"')
    os.system('echo "{}"'.format(msg))
    if index == 1:
        os.system('echo "{}"'.format("=" * len(msg)))
    elif index == 2:
        os.system('echo "{}"'.format("-" * len(msg)))
    elif index == 3:
        os.system('echo "{}"'.format("." * min(len(msg), 7)))
    else:
        os.system('echo "{}"'.format(msg))
    os.system('echo "\n"')


def sh(cmd):
    try:
        result = call(cmd, shell=True)
        if result != 0:
            raise OSError()
    except subprocess.CalledProcessError as e:
        _print("Error executing command: " + cmd, index=None)
        _print(e, index=None)
        exit(1)
    except OSError as e:
        _print("Error executing command: " + cmd, index=None)
        _print(e, index=None)
        exit(1)


class PrometheusHost(object):
    prometheus_config = {"version": "2.5.0", "path": "/opt/prometheus"}

    def download(self):
        sh("apt install -y supervisor")
        if not os.path.isdir(self.prometheus_config["path"]):
            sh(
                """wget https://github.com/prometheus/prometheus/releases/download/v{version}/prometheus-{version}.linux-amd64.tar.gz &&
                         tar xvfz prometheus-{version}.linux-amd64.tar.gz &&
                         mkdir -p {path} && rm -rf -p {path} &&
                         mv prometheus-{version}.linux-amd64 {path}""".format(
                    version=self.prometheus_config["version"], path=self.prometheus_config["path"]
                )
            )

    def configure(self):
        yml = """
    global:
      scrape_interval:     15s # By default, scrape targets every 15 seconds.

      # Attach these labels to any time series or alerts when communicating with
      # external systems (federation, remote storage, Alertmanager).
      external_labels:
        monitor: 'codelab-monitor'

    # A scrape configuration containing exactly one endpoint to scrape:
    # Here it's Prometheus itself.
    scrape_configs:
      # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
      - job_name: 'prometheus'

        # Override the global default and scrape targets from this job every 5 seconds.
        scrape_interval: 5s

        static_configs:
          - targets: ['localhost:9090']"""

        os.chdir(self.prometheus_config["path"])
        if not os.path.isfile("prometheus.yml"):
            with open("prometheus.yml", "w") as file:
                file.write(yml)

    def start(self):
        os.chdir(self.prometheus_config["path"])
        sh("supervisorctl reload")


class PrometheusAgent(object):
    """
    Helper to configure the prometheus data agregation agents:

      1. node-exporter, prometheus server monitor (localhost:9100)
      2. cadvisor, contaienr monitor (localhost:9200)

    This does not currently assist in setting up DNS, virtual hosts, or
    supervisor processes.
    """

    cadvisor = {"path": "/opt/cadvisor"}
    node_exporter_conf = {"version": "0.17.0", "path": "/opt/prometheus/node-exporter"}

    def download(self):
        sh("apt install -y supervisor")

        if not os.path.isdir(self.cadvisor["path"]):
            sh("mkdir -p {}".format(self.cadvisor["path"]))

        if not os.path.isfile(self.node_exporter_conf["path"] + "/node_exporter"):
            sh(
                """wget https://github.com/prometheus/node_exporter/releases/download/v{version}-rc.0/node_exporter-{version}-rc.0.linux-amd64.tar.gz &&
                         tar xvfz node_exporter-{version}-rc.0.linux-amd64.tar.gz &&
                         mkdir -p {path} && rm -rf {path} &&
                         mv node_exporter-{version}-rc.0.linux-amd64 {path} &&
                         rm -rf node_exporter-{version}-rc.0.linux-amd64.tar.gz""".format(
                    version=self.node_exporter_conf["version"], path=self.node_exporter_conf["path"]
                )
            )

    def configure(self):
        yml = """
version: '2'

services:
  cadvisor:
    image: google/cadvisor:v0.29.0
    restart: always
    ports:
      - "9200:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro"""

        os.chdir(self.cadvisor["path"])
        if not os.path.isfile("docker-compose.yml"):
            with open("docker-compose.yml", "w") as file:
                file.write(yml)

        with open("/etc/supervisor/supervisord.conf", "r") as supervisor_config:
            if "program:prometheus_exporter" not in supervisor_config.read():
                sh(
                    'echo "\n[program:prometheus_exporter]\ncommand=/opt/prometheus/node-exporter/node_exporter" >> /etc/supervisor/supervisord.conf'
                )

    def start(self):
        # Start the node-exporter process which should be connected to a
        # supervisor process via /etc/supervisor.conf
        sh("supervisorctl restart prometheus_exporter")

        # Start the cadvisor monitor...
        os.chdir(self.cadvisor["path"])
        sh("sudo docker-compose up -d")


action = sys.argv[1]
if action == "configure.host":
    host = PrometheusHost()
    host.download()
    host.configure()
    host.start()

if action == "configure.agent":
    agent = PrometheusAgent()
    agent.download()
    agent.configure()
    agent.start()

from kubernetes import config
from kubernetes.client.rest import ApiException
from pprint import pprint
from pyhelm.tiller import Tiller
from pyhelm.repo import repo_index
from .git_values import GitValues
import kubernetes.client
import time
from kubernetes.stream import stream
import json
import os
from .yaml_utils import data_to_yaml
from collections import OrderedDict

class ReckonerFileCreator:
    def __init__(self, namespace, region, download_path, repositories, envname, colour, output_file, use_latest_chart_version = False):
        self.namespace = namespace
        self.region = region
        self.download_path = download_path
        self.envname = envname
        self.colour = colour
        self.output_file = output_file
        self.use_latest_chart_version = use_latest_chart_version
        self.reckoner_data = OrderedDict({
            "namespace": self.namespace,
            "repositories": {
                "stable": "https://kubernetes-charts.storage.googleapis.com/"
            },
            "minimum_versions": {
                "helm": "2.10.0",
                "autohelm": "0.6.5"
            },
            "charts": OrderedDict()
        })
        self.repository_charts = {}
        self.repository_chart_versions = {}
        for repository, url in repositories.items():
            self.reckoner_data['repositories'][repository] = url
            self.repository_charts[repository] = {}
            for chart_name, chart_data in repo_index(url)['entries'].items():
                self.repository_charts[repository][chart_name] = chart_data

    def create(self):
        for release in self.get_releases():
            self.reckoner_data['charts'][release.name] = {
                "chart": release.chart.metadata.name,
                "repository": self.get_repository_for_chart(release.chart.metadata.name),
                "set-values": self.get_chart_values(release),
                "files": self.get_value_files_for_release(release),
            }
            if self.use_latest_chart_version == True:
                self.reckoner_data['charts'][release.name]['version'] = self.get_version_for_chart(release.chart.metadata.name)
            else:
                self.reckoner_data['charts'][release.name]['version'] = release.chart.metadata.version

        output = open(self.output_file, "w")
        output.write(data_to_yaml(self.reckoner_data))
        output.close()

    def get_chart_values(self, release):
        return {
            "fullnameOverride": self.get_full_name_override(release)
        }

    def get_full_name_override(self, release):
        return release.name.replace(self.namespace + "-", '')

    def get_value_files_for_release(self, release):
        value_files = []
        gv = GitValues(
            namespace=self.namespace,
            chart=release.chart.metadata.name,
            app=self.get_full_name_override(release),
            region=self.region, extra_files=["_system"],
            download_path=self.download_path,
            colour=self.colour,
            envname=self.envname,
            download_once=True
        )
        gv.download_values(dest=self.download_path)
        path_prefix = os.path.join(self.download_path, '')
        value_files = gv.get_existing_files()

        return value_files

    def get_repository_for_chart(self, chart_name):
        for repository, repository_charts in self.repository_charts.items():
            if chart_name in repository_charts.keys():
                return repository

        return None

    def get_version_for_chart(self, chart_name):
        for repository, repository_charts in self.repository_charts.items():
            if chart_name in repository_charts.keys():
                return repository_charts[chart_name][0]['version']

        return None

    def get_releases(self):
        if not hasattr(self, 'releases'):
            tiller = Tiller('127.0.0.1')
            self.releases = tiller.list_releases(namespace=self.namespace)

        return self.releases

    def forward_tiller_port(self):
        tiller_pod = self.get_tiller_pod()
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient())
        name = tiller_pod.metadata.name
        namespace = tiller_pod.metadata.namespace
        ports = 44134
        try:
            print("Forwarding port")
            api_response = stream(api_instance.connect_get_namespaced_pod_portforward, name=name, namespace=namespace, ports=ports)
            print("Forwarded port")
            while api_response.is_open():
                api_response.update(timeout=1)
                if api_response.peek_stdout():
                    print("STDOUT: %s" % api_response.read_stdout())
                if api_response.peek_stderr():
                    print("STDERR: %s" % api_response.read_stderr())
                print(pyhelm.tiller.list_releases())
                resp.close()

        except ApiException as e:
            print("Exception when calling CoreV1Api->connect_get_namespaced_pod_portforward: %s\n" % e)


    def get_tiller_pod(self):
        label_selector = "app=helm"
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient())
            api_response = api_instance.list_namespaced_pod(
                namespace="kube-system",
                label_selector=label_selector
            )
            return api_response.items[0]
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
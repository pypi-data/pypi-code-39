#
# Copyright (c) 2018, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from itertools import groupby

from neptune.generated.swagger_client import SystemMetricPoint, SystemMetricValues


class MetricReportSender(object):
    def __init__(self, api_service, experiment_id, metrics_from_api):
        self.__api_service = api_service
        self.__experiment_id = experiment_id
        self.__metrics_by_name = {metric.name: metric for metric in metrics_from_api}

    def send(self, metric_reports):
        """
        :param metric_reports: list[MetricReport]
        """
        metric_values = self.__collect_system_metric_values(metric_reports)
        self.__send_system_metric_values(metric_values)

    def __collect_system_metric_values(self, metric_reports):
        return [
            SystemMetricValues(
                metric_id=self.__metric_id(report.metric),
                series_name=gauge_name,
                values=[
                    SystemMetricPoint(x=self.__time_to_millis(metric_value.timestamp), y=metric_value.value)
                    for metric_value in metric_values
                ]
            )
            for report in metric_reports
            for gauge_name, metric_values in groupby(report.values, lambda value: value.gauge_name)
        ]

    def __metric_id(self, metric):
        return self.__metrics_by_name.get(metric.name).id

    def __send_system_metric_values(self, metric_values):
        self.__api_service.send_system_metric_values(self.__experiment_id, metric_values)

    @staticmethod
    def __time_to_millis(timestamp):
        return int(timestamp * 1000.0)

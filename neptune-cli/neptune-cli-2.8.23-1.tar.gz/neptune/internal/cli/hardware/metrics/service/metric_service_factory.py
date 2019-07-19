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

from neptune.internal.cli.hardware.gauges.gauge_factory import GaugeFactory
from neptune.internal.cli.hardware.gpu.gpu_monitor import GPUMonitor
from neptune.internal.cli.hardware.metrics.metrics_factory import MetricsFactory
from neptune.internal.cli.hardware.metrics.reports.metric_reporter_factory import MetricReporterFactory
from neptune.internal.cli.hardware.metrics.service.metric_report_sender import MetricReportSender
from neptune.internal.cli.hardware.metrics.service.metric_service import MetricService
from neptune.internal.cli.hardware.resources.system_resource_info_factory import SystemResourceInfoFactory


class MetricServiceFactory(object):
    def __init__(self, api_service, api_service_factory, os_environ):
        self.__api_service = api_service
        self.__api_service_factory = api_service_factory
        self.__os_environ = os_environ

    def create(self, gauge_mode, experiment_id, reference_timestamp):
        system_resource_info = SystemResourceInfoFactory(
            gpu_monitor=GPUMonitor(), os_environ=self.__os_environ
        ).create(gauge_mode=gauge_mode)

        gauge_factory = GaugeFactory(gauge_mode=gauge_mode)
        metrics_factory = MetricsFactory(gauge_factory=gauge_factory, system_resource_info=system_resource_info)
        metrics = metrics_factory.create_metrics_container().metrics()

        api_metrics = [
            self.__api_service.create_system_metric(experiment_id, metric.to_api_model())
            for metric in metrics
        ]

        metric_reporter = MetricReporterFactory(reference_timestamp).create(metrics=metrics)

        return MetricService(
            metric_reporter=metric_reporter,
            metric_sender=MetricReportSender(
                api_service=self.__api_service_factory.create_services(with_retries=False).api_service,
                experiment_id=experiment_id,
                metrics_from_api=api_metrics
            )
        )

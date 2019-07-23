from ioflow.performance_reporter.performance_reporter_base import \
    PerformanceReporterBase


class RawPerformanceReporter(PerformanceReporterBase):
    def log_performance(self, key, value):
        print("{} => {}".format(key, value))

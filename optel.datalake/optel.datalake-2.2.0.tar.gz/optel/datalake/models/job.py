from abc import ABC

from pkg_resources import iter_entry_points

from optel.datalake.utils import parallelize_pyspark_scheduling


class JobConfiguration(ABC):
    pass


class Job:
    def __init__(self, configuration: JobConfiguration):
        self.configuration = configuration

    def execute_from_entrypoints_group(self, group_name: str) -> None:
        """
        The group should return functions that expects a JobConfiguration,
        it should use that JobConfiguration to create a pipeline object
        and return it.
        """
        entry_points = iter_entry_points(group=group_name)

        get_pipelines_functions = [
            entry_point()
            for entry_point in entry_points
        ]

        pipelines = [
            get_pipeline(self.configuration)
            for get_pipeline in get_pipelines_functions
        ]

        execution_functions = [
            pipeline.execute
            for pipeline in pipelines
        ]

        parallelize_pyspark_scheduling(
            execution_functions,
        )

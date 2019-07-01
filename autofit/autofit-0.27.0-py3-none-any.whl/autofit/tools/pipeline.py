import logging

from autofit import exc

logger = logging.getLogger(__name__)


class ResultsCollection(object):

    def __init__(self):
        """
        A collection of results from previous phases. Results can be obtained using an index or the name of the phase
        from whence they came.
        """
        self.__result_list = []
        self.__result_dict = {}

    @property
    def last(self):
        """
        The result of the last phase
        """
        if len(self.__result_list) > 0:
            return self.__result_list[-1]
        return None

    @property
    def first(self):
        """
        The result of the first phase
        """
        if len(self.__result_list) > 0:
            return self.__result_list[0]
        return None

    def add(self, phase_name, result):
        """
        Add the result of a phase.

        Parameters
        ----------
        phase_name: str
            The name of the phase
        result
            The result of that phase
        """
        self.__result_list.append(result)
        self.__result_dict[phase_name] = result

    def __getitem__(self, item):
        """
        Get the result of a previous phase by index

        Parameters
        ----------
        item: int
            The index of the result

        Returns
        -------
        result: Result
            The result of a previous phase
        """
        return self.__result_list[item]

    def __len__(self):
        return len(self.__result_list)

    def from_phase(self, phase_name):
        """
        Returns the result of a previous phase by its name

        Parameters
        ----------
        phase_name: str
            The name of a previous phase

        Returns
        -------
        result: Result
            The result of that phase

        Raises
        ------
        exc.PipelineException
            If no phase with the expected result is found
        """
        try:
            return self.__result_dict[phase_name]
        except KeyError:
            raise exc.PipelineException(
                "No previous phase named {} found in results ({})".format(
                    phase_name,
                    ", ".join(
                        self.__result_dict.keys()
                    )
                )
            )

    def __contains__(self, item):
        return item in self.__result_dict


class Pipeline(object):

    def __init__(self, pipeline_name, *phases):
        """
        A pipeline of phases to be run sequentially. Results are passed between phases. Phases must have unique names.

        Parameters
        ----------
        pipeline_name: str
            The phase_name of this pipeline
        """
        self.pipeline_name = pipeline_name
        self.phases = phases
        for phase in phases:
            if not hasattr(phase, "pipeline_name"):
                phase.pipeline_name = pipeline_name
        phase_names = [phase.phase_name for phase in phases]
        if len(set(phase_names)) < len(phase_names):
            raise exc.PipelineException(
                "Cannot create pipelines with duplicate phase names. ({})".format(
                    ", ".join(phase_names)))

    def __getitem__(self, item):
        return self.phases[item]

    def __add__(self, other):
        """
        Compose two runners

        Parameters
        ----------
        other: Pipeline
            Another pipeline

        Returns
        -------
        composed_pipeline: Pipeline
            A pipeline that runs all the  phases from this pipeline and then all the phases from the other pipeline
        """
        return self.__class__("{} + {}".format(self.pipeline_name, other.pipeline_name),
                              *(self.phases + other.phases))

    def run_function(self, func, data_name=None):
        """
        Run the function for each phase in the pipeline.

        Parameters
        ----------
        data_name
        func
            A function that takes a phase and prior results, returning results for that phase

        Returns
        -------
        results: ResultsCollection
            A collection of results
        """
        results = ResultsCollection()
        for i, phase in enumerate(self.phases):
            logger.info(
                "Running Phase {} (Number {})".format(phase.optimizer.phase_name, i))
            phase.save_metadata(data_name, self.pipeline_name)
            name = phase.phase_name
            results.add(name, func(phase, results))
        return results

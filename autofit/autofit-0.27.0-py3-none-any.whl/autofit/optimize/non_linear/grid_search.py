import ast
import os

import numpy as np

from autofit import conf, exc
from autofit.optimize import optimizer as opt
from autofit.optimize.non_linear.non_linear import logger
from autofit.optimize.non_linear.non_linear import NonLinearOptimizer, Result, IntervalCounter, persistent_timer


class GridSearch(NonLinearOptimizer):

    def __init__(self, phase_name, phase_tag=None, phase_folders=tuple(), step_size=None, model_mapper=None,
                 grid=opt.grid):
        """
        Optimise by performing a grid search.

        Parameters
        ----------
        step_size: float | None
            The step size of the grid search in hypercube space.
            E.g. a step size of 0.5 will give steps 0.0, 0.5 and 1.0
        model_mapper: cls
            The model mapper class (used for testing)
        phase_name: str
            The name of run (defaults to 'phase')
        grid: function
            A function that takes a fitness function, dimensionality and step size and performs a grid search
        """
        super().__init__(phase_name=phase_name, phase_tag=phase_tag, phase_folders=phase_folders,
                         model_mapper=model_mapper)
        self.step_size = step_size or self.config("step_size", float)
        self.grid = grid

    def copy_with_name_extension(self, extension):
        name = "{}/{}".format(self.phase_name, extension)
        new_instance = self.__class__(phase_name=name, phase_folders=self.phase_folders, model_mapper=self.variable,
                                      step_size=self.step_size)
        new_instance.grid = self.grid
        return new_instance

    class Result(Result):
        def __init__(self, result, instances, previous_variable, gaussian_tuples):
            """
            The result of an grid search optimization.

            Parameters
            ----------
            result: Result
                The result
            instances: [mm.ModelInstance]
                A model instance for each point in the grid search
            """
            super().__init__(result.constant, result.figure_of_merit, previous_variable, gaussian_tuples)
            self.instances = instances

        def __str__(self):
            return "Analysis Result:\n{}".format(
                "\n".join(["{}: {}".format(key, value) for key, value in self.__dict__.items()]))

    class Fitness(NonLinearOptimizer.Fitness):
        def __init__(self, nlo, analysis, instance_from_unit_vector, image_path, save_results,
                     checkpoint_count=0, best_fit=-np.inf, best_cube=None):
            super().__init__(nlo, analysis, image_path)
            self.instance_from_unit_vector = instance_from_unit_vector
            self.total_calls = 0
            self.checkpoint_count = checkpoint_count
            self.save_results = save_results
            self.best_fit = best_fit
            self.best_cube = best_cube
            self.all_fits = {}
            grid_results_interval = conf.instance.general.get('output', 'grid_results_interval', int)

            self.should_save_grid_results = IntervalCounter(grid_results_interval)
            if self.best_cube is not None:
                self.fit_instance(self.instance_from_unit_vector(self.best_cube))

        def __call__(self, cube):
            try:
                self.total_calls += 1
                if self.total_calls <= self.checkpoint_count:
                    #  TODO: is there an issue here where grid_search will forget the previous best fit?
                    return -np.inf
                instance = self.instance_from_unit_vector(cube)
                fit = self.fit_instance(instance)
                self.all_fits[cube] = fit
                if fit > self.best_fit:
                    self.best_fit = fit
                    self.best_cube = cube
                self.nlo.save_checkpoint(self.total_calls, self.best_fit, self.best_cube)
                if self.should_save_grid_results():
                    self.save_results(self.all_fits.items())
                return fit
            except exc.FitException:
                return -np.inf

    @property
    def checkpoint_path(self):
        return "{}/.checkpoint".format(self.path)

    def save_checkpoint(self, total_calls, best_fit, best_cube):
        with open(self.checkpoint_path, "w+") as f:
            def write(item):
                f.writelines("{}\n".format(item))

            write(total_calls)
            write(best_fit)
            write(best_cube)
            write(self.step_size)
            write(self.variable.prior_count)

    @property
    def is_checkpoint(self):
        return os.path.exists(self.checkpoint_path)

    @property
    def checkpoint_array(self):
        with open(self.checkpoint_path) as f:
            return f.readlines()

    @property
    def checkpoint_count(self):
        return int(self.checkpoint_array[0])

    @property
    def checkpoint_fit(self):
        return float(self.checkpoint_array[1])

    @property
    def checkpoint_cube(self):
        return ast.literal_eval(self.checkpoint_array[2])

    @property
    def checkpoint_step_size(self):
        return float(self.checkpoint_array[3])

    @property
    def checkpoint_prior_count(self):
        return int(self.checkpoint_array[4])

    @persistent_timer
    def fit(self, analysis):
        self.save_model_info()

        checkpoint_count = 0
        best_fit = -np.inf
        best_cube = None

        if self.is_checkpoint:
            if not self.checkpoint_prior_count == self.variable.prior_count:
                raise exc.CheckpointException("The number of dimensions does not match that found in the checkpoint")
            if not self.checkpoint_step_size == self.step_size:
                raise exc.CheckpointException("The step size does not match that found in the checkpoint")

            checkpoint_count = self.checkpoint_count
            best_fit = self.checkpoint_fit
            best_cube = self.checkpoint_cube

        def save_results(all_fit_items):
            results_list = [self.variable.param_names + ["fit"]]
            for item in all_fit_items:
                results_list.append([*self.variable.physical_vector_from_hypercube_vector(item[0]), item[1]])

            with open("{}/results".format(self.phase_output_path), "w+") as f:
                f.write("\n".join(map(lambda ls: ", ".join(
                    map(lambda value: "{:.2f}".format(value) if isinstance(value, float) else str(value), ls)),
                                      results_list)))

        fitness_function = GridSearch.Fitness(self,
                                              analysis,
                                              self.variable.instance_from_unit_vector,
                                              self.image_path,
                                              save_results,
                                              checkpoint_count=checkpoint_count,
                                              best_fit=best_fit,
                                              best_cube=best_cube)

        logger.info("Running grid search...")
        self.grid(fitness_function, self.variable.prior_count, self.step_size)

        logger.info("grid search complete")
        self.backup()

        res = fitness_function.result

        instances = [(self.variable.instance_from_unit_vector(cube), fit) for cube, fit in
                     fitness_function.all_fits.items()]

        # Create a set of Gaussian priors from this result and associate them with the result object.
        res = GridSearch.Result(res, instances, self.variable, [(mean, 0) for mean in fitness_function.best_cube])

        analysis.visualize(instance=res.constant, image_path=self.image_path, during_analysis=False)

        return res
from cnvrg.modules.cnvrg_job import CnvrgJob, LOGS_TYPE_OUTPUT, LOGS_TYPE_ERROR
import cnvrg.helpers.param_build_helper as param_build_helper
from cnvrg.modules.project import Project
import cnvrg.helpers.logger_helper as logger_helper
import cnvrg.helpers.string_helper as string_helper
from cnvrg.modules.errors import UserError
import cnvrg.helpers.apis_helper as apis_helper
import cnvrg.helpers.spawn_helper as spawn_helper
import cnvrg.helpers.control_stdout_helper as control_stdout_helper
import cnvrg.helpers.env_helper as env_helper
import cnvrg.helpers.chart_show_helper as chart_show_helper
from cnvrg.helpers.env_helper import in_experiment, CURRENT_JOB_ID
from cnvrg.helpers.url_builder_helper import url_join
from cnvrg.helpers.param_helper import wrap_string_to_list
from cnvrg.helpers.libs_helper import check_if_lib_exists
from enum import Enum
from typing import List
import numpy as np
import os
import time


class TagType(Enum):
    SINGLE_TAG = "single"
    LINECHART_TAG = "linechart"



class Experiment(CnvrgJob):
    def __init__(self, experiment=None):
        owner, project_slug, slug = param_build_helper.parse_params(experiment, param_build_helper.EXPERIMENT)
        if not in_experiment() and not slug:
            raise UserError("Cant create an experiment without slug and outside experiment run")
        slug = slug or CURRENT_JOB_ID
        super(Experiment, self).__init__(slug, env_helper.EXPERIMENT, Project(url_join(owner, project_slug)))
        self.__data = self.__get_experiment()

    @staticmethod
    def init(project=None, **kwargs):
        project = project or Project()
        resp = apis_helper.post(url_join(project.get_base_url(), 'experiments', 'local'),
                                data={"commit": project.get_current_commit(), **kwargs, **env_helper.get_origin_job()})
        e = resp.get("experiment")
        exp = Experiment(url_join(project.get_project_name(), e.get("slug")))
        logger_helper.log_message("Experiment {title} is running, monitor live at: {url}".format(title=exp['title'], url=exp.href()))
        return exp

    @staticmethod
    def __run_callable(callable, title=None, project=None, cwd=None, library=None):
        experiment = Experiment.init(title=title, project=project, library=library)
        exit_status = control_stdout_helper.run_callable(callable, callback=lambda x: experiment.log(x))
        experiment.finish(exit_status=exit_status)
        return experiment

    @staticmethod
    def __run_local(cmd, **kwargs):
        callable = lambda: spawn_helper.run_sync(cmd, print_output=True, cwd=kwargs["cwd"])
        return Experiment.__run_callable(callable, **kwargs)

    @staticmethod
    def run(command=None, callable=None, title=None, project=None, compute=None, computes=None, datasets=None, dataset=None, local=False, library=None, working_directory=None):
        project = project or Project()
        ## support
        computes = computes or wrap_string_to_list(computes) or wrap_string_to_list(compute)
        datasets = datasets or wrap_string_to_list(datasets) or wrap_string_to_list(dataset)

        if callable:
            return Experiment.__run_callable(callable, title=title, project=project, library=library)
        elif local:
            return Experiment.__run_local(cmd=command, title=title, project=project, cwd=working_directory, library=library)
        else:
            e = project.run_experiment(command, title=title, templates=computes, datasets=datasets, library=library)
            return Experiment(e.get("slug"))


    def log_param(self, key, value=None):
        tag_data = {
            "key": key,
            "value": value,
            "type": TagType.SINGLE_TAG.value
        }
        self.__send_tag(tag_data)

    def __dict__(self):
        return self.__data

    def log_metric(self, key, Ys: List, Xs: List=None, grouping: List=None, x_axis=None, y_axis=None) -> None:
        """
        a function which can tag an experiment with a chart
        :param key: the name of the chart
        :param Ys: [y1, y2, y3, y4] (float)
        :param Xs: [x1, x2, x3, x4] (date, integer, null)
        :param grouping: [g1, g2, g3, g4]
        :param x_axis: rename the x_axis of the chart
        :param y_axis:rename the y_axis of the chart
        :return:
        """
        if isinstance(Xs, np.ndarray): Xs = Xs.tolist()
        if isinstance(Ys, np.ndarray): Ys = Ys.tolist()
        tag_data = {
            "ys": Ys,
            "xs": Xs,
            "key": key,
            "grouping": grouping,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "type": TagType.LINECHART_TAG.value,
        }
        self.__send_tag(tag_data)

    def logs(self, callback=None, poll_every=5):
        job_logs, experiment_is_running = self.__fetch_logs(0)
        offset = len(job_logs)
        callback = callback or logger_helper.log_cnvrg_log
        [callback(l) for l in job_logs]
        while experiment_is_running:
            time.sleep(poll_every)
            job_logs, experiment_is_running = self.__fetch_logs(offset)
            offset += len(job_logs)
            ## filter unknown logs?
            [callback(l) if l else None for l in job_logs]


    def show_chart(self, key, **kwargs):
        """

        :param key: chart_key
        :param kwargs: with_legend, legend_loc
        :return:
        """
        chart = apis_helper.get(url_join(self._base_url(), 'charts', key)).get("chart")

        return chart_show_helper.show_chart(chart, **kwargs)


    def __fetch_logs(self, offset, limit=None):
        resp = apis_helper.get(url_join(self._base_url(), 'logs'), data={"offset": offset, "limit": limit})
        return resp.get("logs"), resp.get("experiment").get("is_running")


    def __send_tag(self,tag_data):
        apis_helper.post(url_join(self._base_url(), 'tags'), data={"tag": tag_data})

    def finish(self, exit_status=None):
        apis_helper.post(url_join(self._base_url(), 'finish'), data={"exit_status": exit_status})

    def href(self):
        return self.__data.get("full_href")

    def open(self):
        if check_if_lib_exists("webbrowser"):
            import webbrowser
            webbrowser.open(self.href())
        else:
            logger_helper.log_message("You can find the experiment in: {href}".format(href=self.href))


    def __get_experiment(self):
        return apis_helper.get(self._base_url()).get("experiment")

    def _base_url(self):
        return url_join(
            #### hackish :D
            self.project.get_base_url(),string_helper.to_snake_case(self.job_type) + "s", self.job_slug
        )

    def __getitem__(self, item):
        return self.__data.get(item)




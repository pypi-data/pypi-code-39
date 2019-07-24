# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import pkg_resources
import os
import re
from typing import Any
from azureml.automl.core.package_utilities import _all_dependencies


PACKAGE_NAME = 'azureml.automl.core'
NumpyParameterType = 'NumpyParameterType'
PandasParameterType = 'PandasParameterType'
AutoMLCondaPackagesList = ['numpy', 'pandas', 'scikit-learn', 'py-xgboost<=0.80']
AutoMLPipPackagesList = ['azureml-train-automl', 'inference-schema']


def _get_child_run_number(automl_run_id: str) -> str:
    match_obj = re.match(r"AutoML_(.*)_(\d+)", automl_run_id)
    if match_obj is None:
        return '0'
    return match_obj.group(2)


def _get_model_id(automl_run_id: str) -> str:
    return automl_run_id.replace('_', '').replace('-', '')[:15] + _get_child_run_number(automl_run_id)


def _get_scoring_file(if_pandas_type: bool, input_sample_str: str,
                      automl_run_id: str, is_forecasting: bool = False) -> str:
    """
    Return scoring file to be used at the inference time.

    If there are any changes to the scoring file, the version of the scoring file should
    be updated in the vendor.

    :return: Scoring python file as a string
    """
    if not is_forecasting:
        scoring_file_path = pkg_resources.resource_filename(
            PACKAGE_NAME, os.path.join('inference', 'score.txt'))
    else:
        scoring_file_path = pkg_resources.resource_filename(
            PACKAGE_NAME, os.path.join('inference', 'score_forecasting.txt'))

    inference_data_type = NumpyParameterType
    if if_pandas_type:
        inference_data_type = PandasParameterType

    content = None
    with open(scoring_file_path, 'r') as scoring_file_ptr:
        content = scoring_file_ptr.read()
        content = content.replace('<<ParameterType>>', inference_data_type)
        content = content.replace('<<input_sample>>', input_sample_str)
        content = content.replace('<<modelid>>', _get_model_id(automl_run_id))

    return content


def _create_conda_env_file() -> Any:
    """
    Return conda/pip dependencies for the current AutoML run.

    If there are any changes to the conda environment file, the version of the conda environment
    file should be updated in the vendor.

    :return: Conda dependencies as string
    """
    from azureml.core.conda_dependencies import CondaDependencies
    sdk_dependencies = _all_dependencies()
    pip_package_list_with_version = []
    for pip_package in AutoMLPipPackagesList:
        if 'azureml' in pip_package:
            if pip_package in sdk_dependencies:
                pip_package_list_with_version.append(pip_package + "==" + sdk_dependencies[pip_package])
        else:
            pip_package_list_with_version.append(pip_package)

    myenv = CondaDependencies.create(conda_packages=AutoMLCondaPackagesList,
                                     pip_packages=pip_package_list_with_version,
                                     pin_sdk_version=False)

    return myenv.serialize_to_string()

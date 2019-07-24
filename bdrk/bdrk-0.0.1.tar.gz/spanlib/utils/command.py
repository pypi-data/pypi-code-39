from typing import List, Mapping

from spanlib.infrastructure.span_config.config_objects.command import SparkSubmitCommand

SPARK_SUBMIT_BIN = "spark-submit"


def generate_command(steps: List[List[str]]) -> str:
    """Creates final command to be run from multiple steps. Joins
    individual steps with `&&` to create a single final command
    to run. Steps are joined in order.

    :param List[List[str]] steps: List of steps to combine
    :return str: Final command to be run including install and script steps
    """
    # Flatten to support empty array for install or script key
    # TODO: [BDRK-303] figure out if we need to shlex.quote + eval subcommand
    flattened_steps = [subcommand for step in steps for subcommand in step]
    serve_command = " && ".join(flattened_steps)

    return serve_command


def _make_spark_config_arguments(spark_configs: Mapping[str, str]) -> List[str]:
    # TODO: [BDRK-311] add validation for allow config fields
    result = []
    for name, value in spark_configs.items():
        result.append("--conf")
        result.append(f"{name}={value}")
    return result


def _make_spark_settings_arguments(spark_settings: Mapping[str, str]) -> List[str]:
    result = []
    for name, value in spark_settings.items():
        result.append(f"--{name} {value}")
    return result


def make_spark_run_command(
    spark_system_config: Mapping[str, str],
    spark_system_settings: Mapping[str, str],
    install_script: List[str],
    command: SparkSubmitCommand,
) -> str:
    spark_config = {**spark_system_config, **command.conf}
    spark_settings = {**spark_system_settings, **command.settings}

    spark_submit_options = _make_spark_config_arguments(
        spark_config
    ) + _make_spark_settings_arguments(spark_settings)
    # FIXME: [BDRK-334] we're expecting only the script name. We should expand this to be able to
    # run multiple commands
    spark_workload = command.script
    spark_submit_command = f"{SPARK_SUBMIT_BIN} {' '.join(spark_submit_options)} {spark_workload}"

    steps = [install_script, [spark_submit_command]]
    return generate_command(steps)

import pytest
import yaml

@pytest.fixture()
def gitlabciyml():
    config = open(".gitlab-ci.yml", "r")
    gitlabci = yaml.load(config)
    yield gitlabci


def test_cleanup_after_cloud_test(gitlabciyml):
    print("\n")
    stages_definition = gitlabciyml["stages"]

    job_cloud_test = gitlabciyml["run-cloud-tests"]
    job_shutdown_cluster = gitlabciyml["shutdown_cluster"]

    test_stage = stages_definition.index("test")
    cloud_test_stage = stages_definition.index(job_cloud_test["stage"])
    cleanup_stage = stages_definition.index(job_shutdown_cluster["stage"])

    assert test_stage < cloud_test_stage < cleanup_stage

    cloud_test_branches = job_cloud_test["only"]
    cleanup_branches = job_shutdown_cluster["only"]

    assert set(cloud_test_branches) == set(cleanup_branches)

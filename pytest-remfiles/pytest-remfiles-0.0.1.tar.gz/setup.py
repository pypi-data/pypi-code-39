from setuptools import setup

if __name__ == "__main__":
    setup(entry_points=dict(pytest11=["pytest_remfiles = pytest_remfiles._plugin"]))

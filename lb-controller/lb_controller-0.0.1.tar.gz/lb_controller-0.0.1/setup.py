from setuptools import setup

setup(name="lb_controller",
      version="0.0.1",
      install_requires=[
        "kubernetes_asyncio==9.1.0",
        "jinja2==2.10.1",
        "prometheus-client==0.7.1"],
      extras_require={"tests": ["pytest==4.6.3"]})

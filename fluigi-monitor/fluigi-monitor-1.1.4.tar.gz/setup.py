try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="fluigi-monitor",
    version="1.1.4",
    description="Send summary messages of your Luigi jobs to Slack.",
    long_description=open("README.md").read(),
    url="https://github.com/Foristkirito/luigi-monitor",
    author="Hudl",
    author_email="xiaxin0202@foxmail.com",
    license="MIT",
    packages=['fluigi_monitor'],
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    keywords="luigi",
    install_requires=["requests", "luigi"],
    entry_points={
        "console_scripts": ["fluigi-monitor=fluigi_monitor.fluigi_monitor:run"]
    }
    )


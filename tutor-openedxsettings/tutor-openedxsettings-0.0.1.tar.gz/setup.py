from setuptools import setup


setup(
    name="tutor-openedxsettings",
    version="0.0.1",
    license="AGPLv3",
    author="eliteu",
    author_email="code@eliteu.cn",
    description="A Tutor plugin for openedx settings",
    packages=["tutoropenedxsettings"],
    include_package_data=True,
    python_requires=">=3.5",
    entry_points={"tutor.plugin.v0": ["openedx_settings = tutoropenedxsettings.plugin"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

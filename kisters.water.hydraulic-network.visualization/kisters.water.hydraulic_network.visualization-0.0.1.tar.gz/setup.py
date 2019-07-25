import setuptools
from pathlib import Path

with open(Path(__file__).resolve().parent / "README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kisters.water.hydraulic_network.visualization",
    version="0.0.1",
    author="Jesse VanderWees",
    author_email="jesse.vanderwees@kisters-bv.nl",
    description="Visualization library for the Kisters Hydraulic Network Storage service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/kisters/water/hydraulic-network/visualization",
    packages=["kisters.water.hydraulic_network.visualization.bokeh"],
    zip_safe=False,
    install_requires=[
        "bokeh",
        "kisters.water.hydraulic-network.client",
        "kisters.water.hydraulic-network.models",
        "numpy",
        "scipy",
    ],
    package_data={
        "kisters.water.hydraulic_network.visualization.bokeh": [
            "kisters/water/hydraulic_network/visualization/images/*.svg"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
)

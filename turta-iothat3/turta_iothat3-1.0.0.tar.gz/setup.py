import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turta_iothat3",
    version="1.0.0",
    author="Turta LLC",
    author_email="hello@turta.io",
    description="Python Libraries for Turta IoT HAT 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.turta.io/iothat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: System :: Hardware",
    ],
    project_urls={
        'Documentation': 'https://docs.turta.io/raspberry-pi-hats/iot-hat-3',
        'Community': 'https://community.turta.io',
        'GitHub Repository' : 'https://github.com/Turta-io/IoTHAT3',
    },
)
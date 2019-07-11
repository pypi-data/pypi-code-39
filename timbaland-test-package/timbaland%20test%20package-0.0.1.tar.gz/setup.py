import  setuptools

with open("README.md","r") as fh:
    long_descripton = fh.read()
setuptools.setup(
    name = "timbaland test package",
    version = "0.0.1",
    author = "Timbaland",
    long_descripton = long_descripton,
    url="https://github.com/Timbaland8888/SGXY_Esxi6",
    packages = setuptools.find_packages(),
    classifilers = [
        "programming language:python3",
        "Licens:OSI APPROVED",

    ],




)
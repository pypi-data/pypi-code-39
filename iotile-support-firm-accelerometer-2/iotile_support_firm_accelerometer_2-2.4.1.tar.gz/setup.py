from setuptools import setup, find_packages

setup(
    name="iotile_support_firm_accelerometer_2",
    packages=find_packages(include=["iotile_support_firm_accelerometer_2.*", "iotile_support_firm_accelerometer_2"]),
    version="2.4.1",
    install_requires=['bitstring ~= 3.1', 'iotile-core ~= 5.0'],
    entry_points={'iotile.proxy': ['accel1_proxy = iotile_support_firm_accelerometer_2.accel1_proxy'], 'iotile.virtual_device': ['dev_accel1_1 = iotile_support_firm_accelerometer_2.dev_accel1_1'], 'iotile.emulated_tile': ['accel1_1 = iotile_support_firm_accelerometer_2.accel1_1']},
    author="Arch",
    author_email="info@arch-iot.com"
)
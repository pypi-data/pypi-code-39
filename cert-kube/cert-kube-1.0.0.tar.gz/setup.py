from setuptools import setup, find_packages

setup(
    name='cert-kube',
    packages=['cert_kube'],
    description="Certbot plugin for Oracle Cloud Kubernetes",
    long_description="Certbot plugin for Oracle Cloud Kubernetes",
    author="Dilan Tharaka",
    author_email='tharakamd6@gmail.com',
    include_package_data=True,
    version='1.0.0',
    install_requires=[
        'certbot',
        'zope.interface',
    ],
    entry_points={
        'certbot.plugins': [
            'kube_authenticator = cert_kube.kube:Authenticator'
        ],
    },
)
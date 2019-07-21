from setuptools import find_packages, setup


setup(
    name='gym_yahtzee',
    version='1.0.2',
    description='Yahtzee game engine for OpenAI Gym',
    author='Ville Brofeldt',
    author_email='villebro@apache.org',
    maintainer='Ville Brofeldt',
    maintainer_email='villebro@apache.org',
    url='https://github.com/villebro/gym-yahtzee',
    license='MIT',
    packages=find_packages(exclude='tests'),
    install_requires=[
        'gym',
        'pyhtzee',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)

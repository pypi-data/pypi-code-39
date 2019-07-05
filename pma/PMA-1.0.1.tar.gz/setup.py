import re

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('pma/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Version is not set')

if version.endswith(('a', 'b', 'rc')):
    # Append version identifier based on commit count
    try:
        import subprocess

        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

with open('README.md') as f:
    readme = f.read()

setup(
    name="PMA",
    author="Nihaal Sangha (Orangutan)",
    url="https://github.com/OrangutanGaming/PiXL-Maths-App-Farm",
    project_urls={
        # "Documentation": "https://discordpy.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/OrangutanGaming/PiXL-Maths-App-Farm/issues",
    },
    version=version,
    packages=find_packages(),
    license="MIT",
    description="Farms points for the PiXL Maths App",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.5',
    entry_points="""
    [console_scripts]
    pma=pma.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)

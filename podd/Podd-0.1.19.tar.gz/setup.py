import setuptools
from setuptools.command.install import install

from podd.database import bootstrap_app, migrate_db
from podd.settings import Config


class PostInstallCommand(install):
    """Post-installation entry-point."""

    def run(self):
        """Execute migration script."""
        bootstrap_app()
        migrate_db()
        install.run(self)


with open("README.md") as file:
    long_description = file.read()

requirements = ["feedparser", "jinja2", "mutagen", "click", "keyring", "requests"]

setuptools.setup(
    name="Podd",
    version=Config.version,
    author="Alexander Potts",
    author_email="alexander.potts@gmail.com",
    description="A Podcast downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakkso/Podd",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ),
    cmdclass={"install": PostInstallCommand},
    install_requires=requirements,
    entry_points={"console_scripts": ["podd = podd.__main__:podd"]},
    include_package_data=True,
    data_files=[
        (
            "podd/templates",
            [
                "podd/templates/base.txt",
                "podd/templates/base.html",
                "podd/templates/_podcast.html",
            ],
        )
    ],
)

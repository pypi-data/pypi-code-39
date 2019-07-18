from invoke import task
from . import create


@task
def sidney(_, name):
    """ all the jazz - creates everything."""
    from bluemax.sa import database

    create.project(_, name, with_config=True)
    create.tests(_, name)
    database.create(_, name)

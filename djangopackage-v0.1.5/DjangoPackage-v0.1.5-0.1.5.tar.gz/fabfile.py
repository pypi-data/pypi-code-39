from fabric.api import *

# def runserver():
#    local('python3 manage.py runserver')


def run_docker():
    local('sudo docker image build .')
    local('sudo docker-compose up --build')

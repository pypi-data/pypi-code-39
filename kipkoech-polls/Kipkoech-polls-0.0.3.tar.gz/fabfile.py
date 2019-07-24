from fabric.api import local


def cov_pwd():
    local("python3 manage.py runserver")
    #local("coverage run --source='.' manage.py test")
    #local("coverage report")
    local("pwd")

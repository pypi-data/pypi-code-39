
from argparse import ArgumentParser
from os import environ, path, walk
from os.path import normpath, exists
from pprint import pprint
from sys import argv
from xml.etree.ElementTree import parse

NAME_SPACES = {'ns': 'http://maven.apache.org/SETTINGS/1.0.0'}


def text(e, n):
    return e.findtext(f'ns:{n}', namespaces=NAME_SPACES)


def findall(e, n):
    return e.findall(f'.//ns:{n}', namespaces=NAME_SPACES)


def get_settings_info(settings_path):
    e = parse(normpath(settings_path))

    local_repo = text(e, 'localRepository')
    if '${user.home}' in local_repo:
        local_repo = local_repo.replace('${user.home}', environ['HOME'])

    remotes = {text(r, 'id'): text(r, 'url')
               for r in findall(e, 'repository')}

    plugin_remotes = {text(r, 'id'): text(r, 'url')
                      for r in findall(e, 'pluginRepository')}

    mirrors = {text(r, 'id'): text(r, 'url')
               for r in findall(e, 'mirror')}

    print(e.findall('./mirrors/mirror'))
    print(findall(e, 'mirror'))
    print(list(e.getroot().iter('mirrors')))

    return local_repo, {**remotes, **plugin_remotes, **mirrors}


pprint(get_settings_info('/Users/magnus/git-evry/docker.ci/jenkins_home/settings_host.xml'))
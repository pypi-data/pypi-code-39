"""Automate management of Gradle dependency"""
from re import MULTILINE, search
from json import loads
from platform import system
# Codacy raises B404 low severity on next line. Suggestions welcome.
from subprocess import run, PIPE
from requests import get
from .external_dependency import ExternalDependency

class GradleDependency(ExternalDependency):
    """Concrete class for managing Gradle dependency"""

    def existing(self):
        """Return installed Gradle version"""
        # Codacy raises B603 low severity on next line. Suggestions welcome.
        done_proc = run( \
                     ['gradlew.bat' if system() == 'Windows' else 'gradlew', \
                      '-v'], shell=False, text=True, stdout=PIPE)
        output = done_proc.stdout
        version = search('^Gradle (.+)$', output, MULTILINE)
        return version.group(1)

    def latest(self):
        """Return latest Gradle version available"""
        req = get('https://services.gradle.org/versions/current')
        full_json = loads(req.content.decode())
        # json parsing guidance: https://stackoverflow.com/a/7771071
        return full_json['version']

    def update(self, verbose=False):
        """Update installed Gradle version to latest if necessary"""
        old = self.existing()
        new = self.latest()
        if verbose:
            print('existing Gradle ==> ' + old)
            print('latest Gradle   ==> ' + new)
        if old == new:
            if verbose:
                print('Gradle update not necessary')
        else:
            # Gradle update guidance:
            #    blog.nishtahir.com/2018/04/15/
            #       how-to-properly-update-the-gradle-wrapper
            # Codacy raises B603 low severity on next line. Suggestions welcome.
            run(args=['gradlew.bat' if system() == 'Windows' else 'gradlew', \
                      'wrapper', '--gradle-version', new, \
                      '--distribution-type', 'bin'], \
                shell=False)

#! -*- coding: utf-8 -*-

"""

releaseinator is a quick but hopefully useful script to help
pushout and release python packages. It needs to work with mkrepo and
somehow 'validate and clean up' packages to meet best practise, and
will need to use twine to push code up to pypi and push changes to
git.


Validation checks
-----------------

[ ] Series of validation checks 
[ ] do docs exist in readthedocs.org?
[ ] LICENCE, AUTHORS, etc etc


Versions and releases
[ ] Handle updating the VERSION file for a 'bump'
[ ] each commit builds a version x.x.x-RevisionNumber but we only do public releases on x.x.y
[ ] generate release notes and add them to docs
[ ] build a new wheel and push to pypi 

How to release a pacakge (ie todoinator)

* have git repo clean 
* bump version
* push to pypi

"""

import docopt
import semver
import os
import subprocess


def user_message(msg):
    print(msg)


def bump_version(repopath):
    """Visit `repopath` and find a VERSION file, 
    increase that semver by one.

    """
    versionpath = os.path.join(repopath, "VERSION")
    try:
        with open(versionpath) as fo:
            ver = fo.read()
    except:
        user_message("Unable to find / open VERSION file {}".format(versionpath))
        return

    try:
        nextver = semver.bump_patch(ver)
    except ValueError:
        user_message(
            "The version in {} {} is not valid semver".format(versionpath, ver)
        )
        return

    user_message("Current version is {} - hit Y to bump it to {}".format(ver, nextver))
    yn = input("Y/N: ")
    if yn == "Y":
        with open(versionpath, "w") as fo:
            fo.write(nextver)
    else:
        user_message("No action taken")


def get_latest_wheelname(repopath):
    """ """
    files = os.listdir(repopath + "/dist")
    latest = sorted(files)[-1:][0]
    return latest


def upload_to_pypi(repopath):
    """
* sudo pip install twine
 Install to test location
 sudo python setup.py bdist_wheel 
 python -m twine upload --repository-url=https://test.pypi.org/legacy/ dist/<nameofwheel>

 (username and password - ignore kde wallet request?)


real repositry is upload.pypi.org


    """
    # bump version ok
    # rm-rf build/ dist/
    # python setup.py bdist_wheel
    # python -m twine upload --repository-url=https://upload.pypi.org/legacy/ dist/<nameofwheel>
    template = "python -m twine upload --repository-url=https://upload.pypi.org/legacy/ {repopath}/dist/{latestwheelname}"
    latestwheelname = get_latest_wheelname(repopath)
    cmd = template.format(latestwheelname=latestwheelname, repopath=repopath)
    # subprocess.run(cmd)
    print(cmd)
    subprocess.run(cmd, shell=True)


docopt_msg = """
Usage:
    releaseinator.py bump <packagepathroot> 
    releaseinator.py upload2pypi <packagepathroot>

    releaseinator.py (-h | --help )

Options:
    -h --help    Show this screen


"""

if __name__ == "__main__":
    args = docopt.docopt(docopt_msg)
    abspath = os.path.abspath(args["<packagepathroot>"])
    print(args["<packagepathroot>"], abspath)
    if args["bump"]:
        bump_version(abspath)
    if args["upload2pypi"]:
        upload_to_pypi(abspath)

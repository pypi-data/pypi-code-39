import os
import subprocess

def git_log(gitRevisionRange, cwd):
    cmd = subprocess.Popen(['git', 'log', '--oneline', '--no-color', gitRevisionRange], cwd=cwd, stdout=subprocess.PIPE)
    return cmd.stdout

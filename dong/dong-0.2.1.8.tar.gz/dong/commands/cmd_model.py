import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
import json

import click
import dong
from dong import auth
from dong import net
from dong import utils
from dong.decorators import login_required
import dong.httpclient as httpclient
from tabulate import tabulate


@click.group()
def model():
    """Model management."""
    pass

@model.command()
@click.option('-j', '--job-name')
def ls(job_name):
    """jobs listing"""
    (login, password) = auth.get_credential_or_exit()
    headers = net.authorization_headers(password)
    try:
        r = httpclient.get('api/v1/train/{}/'.format(job_name), headers=headers)
        result = r.json()
        train_jobs = [(result['job_name'], result['status'], result['message'])]
        print("\n")
        print(tabulate(train_jobs, headers=['JOB NAME', 'STATUS', 'MESSAGE'], tablefmt='plain'))
        print("\n")

    except Exception as e:
        output = "Can't get any status of training job: {}, stopped.".format(job_name)

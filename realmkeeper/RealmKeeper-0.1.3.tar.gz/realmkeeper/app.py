from flask import Flask, request, jsonify
from realmkeeper import aws
from realmkeeper import ipa
from .config import config
import logging
import sys

app = Flask(__name__)
app.config.from_object(config)

"""ENDPOINTS"""


@app.route('/ping')
def health_check():
    """Check health status."""
    return 'pong'


@app.route('/v1/aws/register',  methods=['POST'])
def register():
    """Register an AWS instance in IPA and return one-time passowrd(OTP)."""
    instance = aws.Instance(request.remote_addr)
    instance.connect_ec2()
    instance.get_info()
    host = ipa.Host(instance.name, instance.private_ip)

    host.hostname = "something"
    host.check()
    if host.exists and instance.state == 'terminated':
        host.deregister()
        host.register()
        instance.set_tags()

    else:
        host.register()
        instance.set_tags()

    response = jsonify({'hostname': host.hostname,
                        'otp': host.otp})
    response.status_code = 401
    return response

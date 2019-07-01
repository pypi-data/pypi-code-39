from flask import Flask, request, jsonify
from .aws import aws_verify_instance, aws_tag_instance
from .ipa import ipa_verify_host, ipa_add_host, ipa_delete_host
from .config import config


app = Flask(__name__)
app.config.from_object(config)

'''
ENDPOINTS
'''


@app.route('/ping')
def health_check():
    return 'pong'


@app.route('/v1/aws/register',  methods=['POST'])
def register():
    '''
    This function registers an AWS instance in IPA and returns a
    one-time passowrd (OTP) to the client
    '''
    instance = aws_verify_instance(
        request.remote_addr)
    if instance:
        hostname = instance.get('hostname')
        if ipa_verify_host(hostname) and \
                instance.get('instance_state') == 'terminated' or \
                instance.get('Unique'):
                ipa_delete_host(hostname)
                registered = ipa_add_host(
                    hostname,
                    request.remote_addr
                    )
                if registered:
                    aws_tag_instance(hostname, instance.get('instance_id'))
                    return registered
        else:
            registered = ipa_add_host(
                hostname,
                request.remote_addr
                )
            if registered:
                aws_tag_instance(hostname, instance.get('instance_id'))
                return registered
    else:
        response = jsonify(
            {'error': 'Instance could not be verified'}
        )
        response.status_code = 403
        return response

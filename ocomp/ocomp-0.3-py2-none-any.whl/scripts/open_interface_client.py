#!python

import json
import os
import argparse

#py client
import open_interface_grpc_client
import uuid

request_id = os.environ.get("OPEN_CLI_REQUEST_ID");
if not request_id:
    request_id = str(uuid.uuid4());

rpc_host = os.environ.get("OPEN_CLI_RPC_HOST");
rpc_port = os.environ.get("OPEN_CLI_RPC_PORT");
profile = os.environ.get("OPEN_CLI_PROFILE");
mode = os.environ.get("OPEN_CLI_MODE");

if not mode:
    if (rpc_host and rpc_port):
        mode = 'RPC'
    else:
        mode = 'CLI'

#ocilp command
def form_oclip_base_cmd():
    oclip_cmd = 'oclip'
    request_id = os.environ.get("OPEN_CLI_REQUEST_ID");
    if request_id:
        oclip_cmd += " --request-id {}".format(request_id)

    return oclip_cmd

OCLIP_CLI = None

def create_oclip_client():
    return open_interface_grpc_client.OpenInterfaceGrpcClient(
                rpc_host,
                rpc_port)

OCLIP_GRPC_CLIENT = None

class OcompException(Exception):
    def __init__(self, code, message):
        super(OcompException, self).__init__()
        self.code = code;
        self.message = message;

def run_oclip_command(product, command, params={}, profile=None):
    if mode == 'RPC':
        global OCLIP_GRPC_CLIENT
        if not OCLIP_GRPC_CLIENT:
            OCLIP_GRPC_CLIENT = create_oclip_client()

        #result = OCLIP_GRPC_CLIENT.remoteCli(request_id=request_id, product=product,  profile=profile, action=command, params=params)
        result = OCLIP_GRPC_CLIENT.invoke(request_id=request_id, product=product,  profile=profile, action=command, params=params)

        if len(result.ListFields()) == 1 :
            error = json.loads(result.ListFields()[0][1]['error'])
            raise OcompException(code = error['error']['code'], message=error['error']['message'])
        else :
            success = result.ListFields()[0][1];
            if not success:
                error = json.loads(result.ListFields()[1][1]['error']);
                raise OcompException(code = error['error']['code'], message=error['error']['message']);

            output = result.ListFields()[1][1]['results'];
            executionId = result.ListFields()[2][1]['execution-id'];
            # print (success, output, error, executionId);
            return output
    else:
        global OCLIP_CLI
        if not OCLIP_CLI:
            OCLIP_CLI = form_oclip_base_cmd()
        CMD = OCLIP_CLI
        CMD += " --product {} {}".format(product, command)
        for name, value in params.items():
            CMD += " --{} {}".format(name, value)
        print CMD
        result = os.popen(CMD).read()
        print result
        return result

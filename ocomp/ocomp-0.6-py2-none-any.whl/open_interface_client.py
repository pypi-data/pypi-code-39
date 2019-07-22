#!/usr/bin/python

import json
import os

class OcompException(Exception):
    def __init__(self, code, message):
        super(OcompException, self).__init__()
        self.code = code;
        self.message = message;

class OCOMP:
    def __init__(self,
                 request_id = os.environ.get("OPEN_CLI_REQUEST_ID"),
                 rpc_host = os.environ.get("OPEN_CLI_RPC_PORT"),
                 rpc_port = os.environ.get("OPEN_CLI_RPC_PORT"),
                 mode=os.environ.get("OPEN_CLI_MODE")):
        self.OCLIP_GRPC_CLIENT = None
        self.OCLIP_CLI = None
        self.request_id = request_id
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port

        if not mode:
            if (rpc_host and rpc_port):
                mode = 'RPC'
            else:
                mode = 'CLI'
        self.mode = mode

    def create_oclip_client(self):
        import open_interface_grpc_client

        return open_interface_grpc_client.OpenInterfaceGrpcClient(
                    self.rpc_host,
                    self.rpc_port)

    def form_oclip_base_cmd(self, request_id=None):
        oclip_cmd = 'oclip'
        if not request_id:
                request_id = self.request_id
        if request_id:
            oclip_cmd += " --request-id {}".format(request_id)

        return oclip_cmd

    def run(self, product, command, params={}, profile=None, request_id=None):
        if self.mode == 'RPC':
            if not self.OCLIP_GRPC_CLIENT:
                self.OCLIP_GRPC_CLIENT = self.create_oclip_client()

            if not request_id:
                request_id = self.request_id

            try:
                #result = self.OCLIP_GRPC_CLIENT.remoteCli(request_id=request_id, product=product,  profile=profile, action=command, params=params)
                result = self.OCLIP_GRPC_CLIENT.invoke(request_id=request_id, product=product,  profile=profile, action=command, params=params)
            except:
                raise OcompException(code='9999', message='Timeout')

            if len(result.ListFields()) == 1 :
                error = json.loads(result.ListFields()[0][1]['error'])
                raise OcompException(code = error['error']['code'], message=error['error']['message'])
            else :
                success = result.ListFields()[0][1];
                if not success:
                    error = json.loads(result.ListFields()[1][1]['error']);
                    raise OcompException(code = error['error']['code'], message=error['error']['message']);

                output = result.ListFields()[1][1]['results'];
                if request_id:
                    executionId = result.ListFields()[2][1]['execution-id'];
                # print (success, output, error, executionId);
                return output
        else:
            if not self.OCLIP_CLI:
                self.OCLIP_CLI = self.form_oclip_base_cmd()
            CMD = self.OCLIP_CLI
            CMD += " --product {} {}".format(product, command)
            for name, value in params.items():
                CMD += " --{} {}".format(name, value)
            print CMD
            result = os.popen(CMD).read()
            print result
            return result

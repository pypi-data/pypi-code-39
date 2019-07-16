"""The Python implementation of the GRPC Open Interface client."""

from __future__ import print_function

import grpc
import uuid

import oclip_pb2
import oclip_pb2_grpc

class OpenInterfaceGrpcClient(object):
    def __init__(self, host, port):
        super(OpenInterfaceGrpcClient, self).__init__()
        self.host = host
        self.port = port
        self.client = None;

    def invoke(self, action, params = {}, request_id = str(uuid.uuid4()), profile = None, product = 'open-cli'):
        if not self.client:
            self.client = oclip_pb2_grpc.OpenInterfaceStub(grpc.insecure_channel(self.host + ':' + self.port))
        options ={'product': product}
        if (profile):
            options['profile'] = profile

        input = oclip_pb2.Input(
            requestId=request_id,
            action=action,
            params=params,
            options = options)

        print (input)
        output = self.client.invoke(input)
        print (output)
        return output;

    def remoteCli(self, action, params = {}, request_id = str(uuid.uuid4()), profile = None, product = 'open-cli'):
        if not self.client:
            self.client = oclip_pb2_grpc.OpenInterfaceStub(grpc.insecure_channel(self.host + ':' + self.port))
        def map2array():
            paramsArray = ['--request-id', request_id, '--product', product, action]
            if params:
                for name, value in params.items():
                    paramsArray.extend(['--' + name, value])
            return paramsArray

        args = oclip_pb2.Args(args=map2array())

        print (args);
        result = self.client.remoteCli(args)
        print(result)
        return result;

def test():
    client = OpenInterfaceGrpcClient('localhost', '50051');
    print ('using cli:', client.remoteCli(action = 'schema-refresh', params={'format': 'json'}))
    print ('using rpc:', client.invoke(action = 'schema-refresh'))

if __name__ == '__main__':
    test()

from resourcify.client import ClientBase
from resourcify.resource import Resource, ResourceDescriptor, Path, CollectionOf
from resourcify.component import Body, Integer, String

from requests import Response
import io

def test_resource_definition():
    @Path('/servers/{server_id}', actions=['get', 'list'])
    class Server(ResourceDescriptor):

        name = Body(String)

    class Client(ClientBase):
        session = 'hello session'
        server = Server()
        
        def request(self, method, urlformat, **kwargs) -> Response :
            print("Request!")
            r = Response()
            r.raw = io.BytesIO(b'{"113":"1"}') 
            r.contents = '"{11:1}"'
            r.status_code = 400
            return r
    
    c = Client()
    print(c.server.list('11'))

    assert True

test_resource_definition()

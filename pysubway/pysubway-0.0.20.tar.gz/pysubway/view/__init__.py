from flask_restful import Resource

try:
    from controller.request import Request
    from errors import IncomingDataValueError
    from utils.package import Package
    from utils.utype import *
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.controller.request import Request
    from pysubway.errors import IncomingDataValueError
    from pysubway.utils.package import Package
    from pysubway.utils.utype import *

__all__ = [
    'ViewBase',
]


class ViewBase(Resource):
    request = Request()
    service = None

    @classmethod
    def set_service(cls, package_path: str, prefix: str) -> Dict[str, Any]:
        return Package(package_path).get_classes(prefix)

    def exec_service(self) -> Dict[str, Any]:
        if not self.service:
            pass
        cls_name, method_name, _ = self.request.service
        exec_method = getattr(self.service.get(cls_name), method_name)
        if not exec_method:
            raise IncomingDataValueError(f'class cls_name {cls_name} do not have method {method_name}')
        return exec_method(self.request.data)

    def get(self):
        return 'hello pysubway ...'

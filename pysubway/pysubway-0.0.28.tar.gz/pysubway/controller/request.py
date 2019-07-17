from flask import request

try:
    from errors import IncomingDataTypeError
    from errors import IncomingDataValueError
    from utils.utype import *
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.errors import IncomingDataTypeError
    from pysubway.errors import IncomingDataValueError
    from pysubway.utils.utype import *


class Request:
    """
    {
      "service":"cls.method",
      "parameter": "...."
    }
    """
    f_service = 'service'

    def __init__(self) -> None:
        self._incoming_data: Dict = dict()

    @property
    def data(self) -> Dict[str, Any]:
        try:
            if not self._incoming_data:
                self._incoming_data = request.json
            return self._incoming_data
        except Exception as e:
            raise IncomingDataTypeError('incoming data must be json')

    @property
    def service(self) -> Tuple[str, str, Optional[List[str]]]:
        service_val = self.data.get(self.f_service)
        if not isinstance(service_val, str):
            raise IncomingDataValueError('service of incoming data is invalid')
        splited = service_val.split('.')
        if len(splited) < 2:
            raise IncomingDataValueError('service of incoming data is wrong.')
        cls_name, method_name, *reserved = splited
        return cls_name, method_name, reserved

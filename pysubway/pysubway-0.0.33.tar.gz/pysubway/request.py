from flask import request

try:
    from errors import IncomingDataValueError
    from utils.utype import *
except (ModuleNotFoundError, ImportError) as e:
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

    @property
    def data(self) -> Any:
        return request.json

    @staticmethod
    def request_json() -> Dict[Any, Any]:
        return request.json

    @property
    def service(self) -> Tuple[str, str, Optional[List[str]]]:
        service_val = request.json.get(self.f_service)
        if not isinstance(service_val, str):
            raise IncomingDataValueError('service of incoming data is invalid')
        splited = service_val.split('.')
        if len(splited) < 2:
            raise IncomingDataValueError('service of incoming data is wrong.')
        cls_name, method_name, *reserved = splited
        return cls_name, method_name, reserved

    @staticmethod
    def get_data(*keys: str) -> Optional[Tuple[Any, ...]]:
        """
        if mimetype == 'application/x-www-form-urlencoded' and front end html example:
            action: request url
            name: name is necessary, name is ImmutableMultiDict item key
            <form role="form" action="/download-file/"
                      target="_self"
                      accept-charset="UTF-8"
                      method="POST"
                      autocomplete="off"
                      enctype="application/x-www-form-urlencoded">

                <textarea name="comment"></textarea>
                <input ..../>
            </form>
        :return:
        """
        if request.mimetype == 'application/x-www-form-urlencoded':
            if isinstance(request.form, dict):
                return tuple(request.form.get(key, '') for key in keys)
            else:
                raise NotImplementedError(f'request.form {request.form} type not support now.')
        elif request.mimetype == 'application/json':
            if isinstance(request.json, dict):
                return tuple(request.json.get(i) for i in keys)
            else:
                raise NotImplementedError(f'request.json {request.json} type not support now.')
        else:
            raise NotImplementedError(f'request.mimetype {request.mimetype} not support now.')

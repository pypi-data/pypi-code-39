from typing import ClassVar, Dict

from flask_restful import abort

try:
    from utils.utype import *
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.utype import *


class Output:
    f_resp_code: ClassVar[str] = 'resp_code'
    f_resp_data: ClassVar[str] = 'resp_data'
    f_resp_msg: ClassVar[str] = 'resp_msg'
    code_success: ClassVar[str] = 'SW0000'
    code_login_failed: ClassVar[str] = 'SW0001'
    code_authentication_failed: ClassVar[str] = 'SW0002'
    code_permission_deny: ClassVar[str] = 'SW0100'
    code_format_error: ClassVar[str] = 'SW0200'
    code_incoming_data_error: ClassVar[str] = 'SW0300'
    code_not_found: ClassVar[str] = 'SW9998'
    code_system_error: ClassVar[str] = 'SW9999'
    code_msg: ClassVar[Dict[str, str]] = {
        # SW0000 成功
        code_success: "成功",
        # SW00xx 登录、认证
        code_login_failed: "登录失败",
        code_authentication_failed: '认证失败',
        # SW01xx 鉴权
        code_permission_deny: "权限不足",
        # SW02格式
        code_format_error: "格式有误",
        # SW03入参
        code_incoming_data_error: "参数错误",
        code_system_error: "系统错误",
        code_not_found: "404 not found",
    }

    def __init__(self, resp_code: str, *args: Dict[str, Any]):
        """
        :return: {
              "resp_code":"SW0000",
              "resp_data":{},
              "resp_msg":"xxxx"
            }
        """
        if resp_code not in self.code_msg:
            raise Exception(f'unknown resp_code {resp_code}')
        self._resp_code = resp_code
        self._resp_msg = self.code_msg[self._resp_code]
        if len(args) <= 1:
            self._resp_data = args[0] if len(args) == 1 else {}
        else:
            resp_data = {}
            for i in args:
                if not isinstance(i, dict):
                    raise Exception('')
                else:
                    resp_data.update(i)
            self._resp_data = resp_data
        self.data = {
            self.f_resp_code: self._resp_code,
            self.f_resp_data: self._resp_data,
            self.f_resp_msg: self._resp_msg
        }

    @classmethod
    def update_code_msg(cls, *args: Dict) -> None:
        for i in args:
            if not isinstance(i, dict):
                raise Exception('args must be dict')
            cls.code_msg.update(i)


class Response:

    def __init__(self) -> None:
        self._abort_code: Dict[str, int] = {
            "SW0002": 401,
            "SW0300": 400,
            "SW9999": 500
        }

    def update_abort_code(self, *args: Dict[str, int]) -> None:
        for i in args:
            if not isinstance(i, dict):
                raise Exception('args must be dict')
            self._abort_code.update(i)

    def abort(self, data: Dict[str, str], new_abort_code: Dict[str, int] = None) -> Dict[str, Any]:
        if new_abort_code:
            self.update_abort_code(new_abort_code)
        http_code = self._abort_code.get(data.get(Output.f_resp_code, ''), '')
        if http_code:
            abort(http_code)
        return data

    @classmethod
    def _resp(cls, code: str, *args: Dict[str, Any]) -> Dict[str, Any]:
        return Output(code, *args).data

    @classmethod
    def success(cls, *args: Dict[str, Any]) -> Dict[str, Any]:
        return cls._resp(Output.code_success, *args)

    @classmethod
    def login_fail(cls) -> Dict[str, Any]:
        """
        登陆失败
        """
        return cls._resp(Output.code_login_failed)

    @classmethod
    def authentication_failed(cls) -> Dict[str, Any]:
        return cls._resp(Output.code_authentication_failed)

    @classmethod
    def permission_deny(cls) -> Dict[str, Any]:
        return cls._resp(Output.code_permission_deny)

    @classmethod
    def format_error(cls) -> Dict[str, Any]:
        return cls._resp(Output.code_format_error)

    @classmethod
    def incoming_data_error(cls) -> Dict[str, Any]:
        return cls._resp(Output.code_incoming_data_error)

    @classmethod
    def system_error(cls) -> Dict[str, Any]:
        """
        权限不足
        """
        return cls._resp(Output.code_system_error)

    @classmethod
    def not_found(cls) -> Dict[str, Any]:
        return cls._resp(Output.code_not_found)

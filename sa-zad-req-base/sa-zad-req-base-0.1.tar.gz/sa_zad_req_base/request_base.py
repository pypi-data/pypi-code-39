from django.core.paginator import Paginator
from django.views import View

from .base_exceptions import ErrorCodeException
from .utils import *
from plusoneauthentication.models import AuthUser, PlusOneUser
from math import *

from rest_framework.utils import json
from abc import ABC, abstractmethod


class RequestBase(View, ABC):
    method = None
    __request = None
    __values = None
    __mandatory_fields = None

    def __init__(self, mandatory_request_fields=None, **kwargs):
        # time.sleep(2)
        super().__init__(**kwargs)
        print(mandatory_request_fields)
        if mandatory_request_fields is None:
            mandatory_request_fields = []
        self.__mandatory_fields = mandatory_request_fields

    def request_method_ok(self):
        raise NotImplementedError('subclasses must override request_method_ok')

    def request_method_not_allowed(self):
        return request_http_error_response(ErrorCode.INVALID_METHOD,
                                           {"method": 'Only ' + str(self.method) + ' requests permitted'})

    def on_fields_missing(self, missing_fields: dict):
        return request_http_error_response(ErrorCode.FIELDS_MISSING, missing_fields)

    def get_device_type(self):
        return self.__request.META.get('HTTP_DEVICE_OS')

    def get_request(self):
        return self.__request

    def get_value(self, key):
        return self.__values.get(key)

    def post(self, request, **kwargs):
        return self.__json_data(request)

    def get(self, request, **kwargs):
        self.__request = request
        self.__values = request.GET
        return self.__process()

    def put(self, request, **kwargs):
        return self.__json_data(request)

    def patch(self, request, **kwargs):
        return self.__json_data(request)

    def __json_data(self, request):
        self.__request = request

        try:
            self.__values = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            pass

        return self.__process()

    def __process(self):
        if self.__request.method != self.method:
            return self.request_method_not_allowed()

        not_found_fields = {}
        for field in self.__mandatory_fields:
            if self.__values is None or self.__values.get(field) is None:
                not_found_fields.update({field: "missing"})

        if len(not_found_fields) > 0:
            return self.on_fields_missing(not_found_fields)

        return self.request_method_ok()


class EmailRequestBase(RequestBase, ABC):
    def get_email(self):
        raise NotImplementedError("Overriding class should implement get_email")

    def get_password(self):
        pass

    def request_method_ok(self):
        try:
            from plusoneauthentication.email_signup import LoginLog
            self.login_log = LoginLog(self.get_email(), self.get_password())
            self.login_log.validate_entry()
            ret = self.user_valid()
            if ret != None:
                return ret
        except ErrorCodeException as e:
            if e.error_code.is_USER_LOCKED_OUT():
                return self.user_locked_out(e.error_code)
            elif e.error_code.is_ACCOUNT_SUSPENDED():
                self.login_log.flag_suspended()
                return self.user_suspended(e.error_code)

    def user_valid(self):
        pass

    def user_locked_out(self, error_code: ErrorCode):
        return self.__throw_error(error_code)

    def user_suspended(self, error_code: ErrorCode):
        return self.__throw_error(error_code)

    def __throw_error(self, error_code: ErrorCode):
        field = {
            "suspended_until": time_json(self.login_log.suspended_until()),
            "suspension_duration": self.login_log.suspension_duration,
            "suspension_count": self.login_log.total_suspensions,
            "try_again_after": self.login_log.try_in()
        }
        return request_http_error_response(error_code, field)


class AuthRequestBase(EmailRequestBase, ABC):
    __activity = None
    __auth_user = None

    def auth_token_not_found(self):
        return request_http_error_response(ErrorCode.AUTH_TOKEN_NOT_FOUND)

    def on_auth_token(self, auth_token):
        pass

    def authorization_failed(self, auth_user):
        return request_http_error_response(ErrorCode.AUTH_TOKEN_EXPIRED)

    def invalid_token(self):
        return request_http_error_response(ErrorCode.INVALID_AUTH_TOKEN)

    def get_user(self) -> PlusOneUser:
        return self.__activity

    def get_auth_user(self) -> AuthUser:
        return self.__auth_user

    def request_method_ok(self):
        return self.__validate(self.get_request())

    def auth_ok(self, auth_user):
        raise NotImplementedError('subclasses must override auth_ok')

    def user_suspended(self, error_code: ErrorCode):
        return self.user_valid()

    def user_valid(self):
        self.__auth_user = self.__auth_user.update_time()
        return self.auth_ok(self.__auth_user)

    def get_email(self):
        return self.__auth_user.user.email

    def __validate(self, request):
        if request.META.get('HTTP_AUTH_TOKEN') is None:
            return self.auth_token_not_found()

        print(request.META.get('HTTP_AUTH_TOKEN'))
        self.on_auth_token(request.META.get('HTTP_AUTH_TOKEN'))
        auth_user = AuthUser.match_auth_token_validity(request.META.get('HTTP_AUTH_TOKEN'))

        if auth_user is not None and auth_user.has_expired:
            return self.authorization_failed(auth_user)
        elif auth_user is None:
            return self.invalid_token()
        elif auth_user is not None and not auth_user.has_expired:
            self.__activity = auth_user.user
            self.__auth_user = auth_user
            return super(AuthRequestBase, self).request_method_ok()


class HybridRequestBase(AuthRequestBase, ABC):
    def invalid_token(self):
        return self.get_auth_failed_response()

    def auth_token_not_found(self):
        return self.get_auth_failed_response()

    def authorization_failed(self, auth_user):
        return self.get_auth_failed_response(auth_user)

    def user_locked_out(self, error_code: ErrorCode):
        return self.get_auth_failed_response(self.get_auth_user())

    def get_auth_failed_response(self, auth_user: AuthUser = None) -> HttpResponse:
        raise NotImplementedError('subclasses must override get_response')


class PageData(RequestBase, ABC):
    def page_response(self, entries):

        try:
            count = int(self.get_value("count"))
        except:
            count = 10

        paginator = Paginator(entries, count)
        pages = paginator.get_page(self.get_value("page"))
        data = self.serialize_data(paginator.page(pages.number))

        if (pages.number == paginator.num_pages):
            next_page = None
        else:
            next_page = pages.number + 1

        if (pages.number == 1):
            prev_page = None
        else:
            prev_page = pages.number - 1

        return JsonHttpResponse(
            {"data": data, "page": pages.number, "next_page": next_page, "prev_page": prev_page, "count": count,
             "max_pages": paginator.num_pages, "total": entries.count()})

    def serialize_data(self, data):
        NotImplementedError("Overriding class should implement serialize_data method")

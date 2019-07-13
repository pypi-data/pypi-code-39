import json
import ssl
import tempfile
import urllib
import urllib.request
import uuid
from datetime import datetime, timedelta
from itertools import chain
from random import randint

import requests
from PIL import Image
from django.core import files
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import (
    MaxLengthValidator, MaxValueValidator, MinLengthValidator,
    MinValueValidator
)
from django.forms.utils import ErrorDict
from django.http import HttpResponseNotAllowed, HttpResponse
from django.utils import timezone
from .codes import ErrorCode


def get_readonly_fields(self):
    return tuple(set(chain.from_iterable(
        (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
        for field in self._meta.get_fields()
        # For complete backwards compatibility, you may want to exclude
        # GenericForeignKey from the results.
        if not (field.many_to_one and field.related_model is None))))


def get_model_fields(self):
    return tuple([f.name for f in self._meta.fields])


def ssl_request(request_url, method=None, data=None, headers=None):
    try:
        ssl_header = {'X-Mashape-Key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}
        if headers is None:
            headers = ssl_header
        else:
            headers.update(ssl_header)

        req = urllib.request.Request(request_url, data=data, method=method,
                                     headers=headers)
        return json.loads(urllib.request.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)).read())
    except Exception as e:
        print(request_url)
        print(e)
        return None


def extract_post_value(request, value):
    return request.POST.get(value, None)


def extract_get_value(request, value):
    return request.GET.get(value, None)


def is_request_method_get(request):
    return check_request_method(request, "GET")


def is_request_method_post(request):
    return check_request_method(request, "POST")


def check_request_method(request, method):
    if request.method != method:
        return HttpResponseNotAllowed('Only ' + method + ' requests permitted')


def time_json(datetime):
    return json.loads(
        json.dumps({"string": str(datetime), "timestamp": int(datetime.timestamp())}))


def is_time_stale(datetime, seconds=0):
    valid_until = datetime + timedelta(seconds=seconds)
    return int(valid_until.timestamp()) < int(timezone.now().timestamp())


def value_validation(value, max, min=0, allow_none=True, field_name=None,
                     min_error_message=None, max_error_message=None, none_string_error_message=None):
    field_name = field_name if field_name != None else "value"

    if none_string_error_message == None:
        none_string_error_message = field_name + " can't be empty"

    if value == None:
        if not allow_none:
            raise Exception(none_string_error_message)
        return value

    if max_error_message == None:
        max_error_message = "Incorrect " + field_name + ". Max value of " + str(max) + " is allowed."

    if min_error_message == None:
        min_error_message = "Incorrect " + field_name + ". Required MIN value is " + str(min) + "."

    MinValueValidator(min, min_error_message)(value)
    MaxValueValidator(max, max_error_message)(value)

    return value


def string_length_validation(string, max_length, min_length=0, allow_none=True, field_name=None,
                             min_error_message=None, max_error_message=None, none_string_error_message=None):
    field_name = field_name if field_name != None else "value"

    if none_string_error_message == None:
        none_string_error_message = field_name + " can't be empty"

    if string == None:
        if not allow_none:
            raise Exception(none_string_error_message)
        return string

    if max_error_message == None:
        max_error_message = "Incorrect " + field_name + " length. Max length " + str(
            max_length) + " is allowed."

    if min_error_message == None:
        min_error_message = "Incorrect " + field_name + " length. Required MIN length is " + str(
            min_length) + "."

    MaxLengthValidator(max_length, max_error_message)(string)
    MinLengthValidator(min_length, min_error_message)(string)

    return string


def get_timestamp_to_timezone(millis):
    try:
        return timestamp_to_timezone(millis)
    except:
        return None


def timestamp_to_timezone(epoch_seconds):
    if epoch_seconds == None:
        raise Exception("None not allowed")
    return timezone.make_aware(datetime.utcfromtimestamp(int(epoch_seconds // 1000)), timezone.utc)


def image_name(file):
    return str(uuid.uuid4()) + "." + str(Image.open(file).format).lower()


def file_download(url) -> File:
    # Steam the image from the url
    request = requests.get(url, stream=True)

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        raise Exception("Something went wrong")

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    return files.File(lf)


def file_size(value):
    limit = 1000 * 1024
    if value.size > limit:
        raise ValidationError(
            "File too large(" + str(value.size / 1024) + " Kb). Size should not exceed " + str(
                limit / 1024) + "  Kb.")


def __request_response_success(data):
    return {"data": data}


def __request_response_error(error_code: ErrorCode, fields: dict = None):
    fields_array = []

    if fields != None:
        # fields_array = []
        for key, value in fields.items():
            fields_array.append({"field": key, "message": value})

    return {"error": {
        "status": error_code.get_http_status_code(),
        "error": error_code.phrase,
        "error_code": error_code.value,
        "description": error_code.description,
        "fields": fields_array
    }}


def request_http_error_response(error_code: ErrorCode, fields: dict = None) -> HttpResponse:
    return JsonHttpResponse(__request_response_error(error_code, fields), error_code.get_http_status_code())


def request_http_response(data, status_code=200) -> HttpResponse:
    return JsonHttpResponse(__request_response_success(data), status_code)


def empty_response() -> HttpResponse:
    return HttpResponse(status=204)


def JsonHttpResponse(serialize_data, status_code=200) -> HttpResponse:
    return HttpResponse(serialize_to_json(serialize_data), content_type="json", status=status_code)


def unknown_error_response(message="") -> HttpResponse:
    return HttpResponse(status=500, content=message)


def serialize_to_json(data):
    return json.dumps(data)


class CallBack():
    def callback(self, call):
        pass

    @staticmethod
    def iterate_list(items: list, callback):

        """
        my_method description

        @type items: list
        @param items: A List

        @:type callback: CallBack
        @:param callback: CallBack

        @rtype: string
        @return: Returns a sentence with your variables in it
        """

        try:
            for item in items:
                callback.callback(item)
        except Exception as e:
            print(str(e))


class RequestParaHelper():
    __mandatory_fields = []

    def __init__(self):
        self.__mandatory_fields.clear()
        self.__mandatory_fields.extend(self.get_mandatory_params())

    def get_mandatory_params(self):
        return []


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def generate_token():
    return uuid.uuid4()


def plural(count: int, singularWord: str, pluralWord: str) -> str:
    if count > 1:
        return pluralWord
    return singularWord


def validation_error_extraction(error: ValidationError):
    str = ""
    for err in error.messages:
        str += err
    return str


def form_error(error_dict: ErrorDict, field_name: str):
    err = (error_dict.get(field_name, "--not found--") or [None])[0]
    return validation_error_extraction(err)


def require_non_none(value, non_none_value):
    if (value == None):
        return non_none_value
    return value

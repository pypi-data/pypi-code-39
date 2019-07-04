import json

import asynctest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from src.pyodstibmivb.odstibmivb import HttpException, ODStibMivb
from tests import mock_requests

API_KEY = "2133c416f69f5acaa67351501153d892"
CONTENT_TYPE = "application/json"


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class TestODStibMivb(AioHTTPTestCase):
    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        async def vehicle_position_1(request):
            response = mock_requests.Response(request.url.path, request.headers)
            return web.Response(
                text=response.text, status=response.status, content_type=CONTENT_TYPE
            )

        app = web.Application()
        app.router.add_get("/{tail:.+}", vehicle_position_1)
        return app

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_vehicle_position_single(self):
        result = await ODStibMivb(API_KEY, self.client).get_vehicle_position("1")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.VEHICLE_POSITION_1))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_vehicle_position_single_int(self):
        result = await ODStibMivb(API_KEY, self.client).get_vehicle_position(1)
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.VEHICLE_POSITION_1))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_vehicle_position_multiple(self):
        result = await ODStibMivb(API_KEY, self.client).get_vehicle_position("1", "5")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.VEHICLE_POSITION_1_5))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_vehicle_position_multiple_int(self):
        result = await ODStibMivb(API_KEY, self.client).get_vehicle_position(1, 5)
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.VEHICLE_POSITION_1_5))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_waiting_time_single(self):
        result = await ODStibMivb(API_KEY, self.client).get_waiting_time("8301")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.WAITING_TIME_8301))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_waiting_time_multiple(self):
        result = await ODStibMivb(API_KEY, self.client).get_waiting_time("8301", "8302")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.WAITING_TIME_8301_8302))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_message_by_line_single(self):
        result = await ODStibMivb(API_KEY, self.client).get_message_by_line("12")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.MESSAGE_BY_LINE_12))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_message_by_line_multiple(self):
        result = await ODStibMivb(API_KEY, self.client).get_message_by_line("12", "17")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.MESSAGE_BY_LINE_12_17))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_stops_by_line_single(self):
        result = await ODStibMivb(API_KEY, self.client).get_stops_by_line("1")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.STOPS_BY_LINE_1))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_stops_by_line_multiple(self):
        result = await ODStibMivb(API_KEY, self.client).get_stops_by_line("1", "5")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.STOPS_BY_LINE_1_5))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_point_detail_single(self):
        result = await ODStibMivb(API_KEY, self.client).get_point_detail("8301")
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.POINT_DETAIL_8301))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_point_detail_multiple(self):
        result = await ODStibMivb(API_KEY, self.client).get_point_detail(
            "8301", "0470F"
        )
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.POINT_DETAIL_8301_0470F))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_message_by_line_with_point_detail_single(self):
        result = await ODStibMivb(
            API_KEY, self.client
        ).get_message_by_line_with_point_detail("32")
        self.assertEqual(
            ordered(result["messages"][0]["content"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_32)["messages"][0]["content"]
            ),
        )
        self.assertEqual(
            ordered(result["messages"][0]["priority"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_32)["messages"][0]["priority"]
            ),
        )
        self.assertEqual(
            ordered(result["messages"][0]["priority"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_32)["messages"][0]["priority"]
            ),
        )
        part1 = json.loads(mock_requests.POINT_DETAIL_10_ARGS_2903F_TO_5801)
        part2 = json.loads(mock_requests.POINT_DETAIL_10_ARGS_5714_TO_5712F)
        part3 = json.loads(mock_requests.POINT_DETAIL_10_ARGS_5711F_TO_626)
        part4 = json.loads(mock_requests.POINT_DETAIL_4_ARGS_5868_TO_636)
        self.assertEqual(
            ordered(result["messages"][0]["points"]),
            ordered(
                part1["points"] + part2["points"] + part3["points"] + part4["points"]
            ),
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_message_by_line_with_point_detail_multiple(self):
        result = await ODStibMivb(
            API_KEY, self.client
        ).get_message_by_line_with_point_detail("12", "32")
        self.assertEqual(
            ordered(result["messages"][0]["content"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_12)["messages"][0]["content"]
            ),
        )
        self.assertEqual(
            ordered(result["messages"][0]["priority"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_12)["messages"][0]["priority"]
            ),
        )
        self.assertEqual(
            ordered(result["messages"][0]["type"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_12)["messages"][0]["type"]
            ),
        )
        self.assertEqual(
            ordered(result["messages"][0]["points"]),
            ordered(json.loads(mock_requests.POINT_DETAIL_6448)["points"]),
        )

        self.assertEqual(
            ordered(result["messages"][1]["content"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_32)["messages"][0]["content"]
            ),
        )
        self.assertEqual(
            ordered(result["messages"][1]["priority"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_32)["messages"][0]["priority"]
            ),
        )
        self.assertEqual(
            ordered(result["messages"][1]["priority"]),
            ordered(
                json.loads(mock_requests.MESSAGE_BY_LINE_32)["messages"][0]["priority"]
            ),
        )
        part1 = json.loads(mock_requests.POINT_DETAIL_10_ARGS_2903F_TO_5801)
        part2 = json.loads(mock_requests.POINT_DETAIL_10_ARGS_5714_TO_5712F)
        part3 = json.loads(mock_requests.POINT_DETAIL_10_ARGS_5711F_TO_626)
        part4 = json.loads(mock_requests.POINT_DETAIL_4_ARGS_5868_TO_636)
        self.assertEqual(
            ordered(result["messages"][1]["points"]),
            ordered(
                part1["points"] + part2["points"] + part3["points"] + part4["points"]
            ),
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_point_detail_incorrect_argument(self):
        with self.assertRaises(HttpException) as context_manager:
            await ODStibMivb(API_KEY, self.client).get_point_detail("/8301/")
        self.assertEqual(context_manager.exception.status_code, 403)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_number_arguments_11(self):
        result = await ODStibMivb(API_KEY, self.client).get_point_detail(
            1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 28
        )
        part1 = json.loads(mock_requests.POINT_DETAIL_10_ARGS)
        part2 = json.loads(mock_requests.POINT_DETAIL_28)
        self.assertEqual(
            ordered(result["points"]), ordered(part1["points"] + part2["points"])
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_number_arguments_10(self):
        result = await ODStibMivb(API_KEY, self.client).get_point_detail(
            1, 2, 3, 4, 5, 6, 7, 8, 9, 15
        )
        self.assertEqual(
            ordered(result), ordered(json.loads(mock_requests.POINT_DETAIL_10_ARGS))
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_point_detail_incorrect_formatted_key(self):
        with self.assertRaises(ValueError):
            await ODStibMivb("123456", self.client)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_point_detail_incorrect_key(self):
        api_instance = ODStibMivb(API_KEY[:-1] + "9", self.client)
        with self.assertRaises(HttpException) as context_manager:
            await api_instance.get_point_detail("8301")
        self.assertEqual(context_manager.exception.status_code, 401)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_invalid_method(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        with self.assertRaises(ValueError):
            await api_instance.do_request("get_message_by_stop", "8301")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_server_wrong_data(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        with self.assertRaises(Exception) as context_manager:
            await api_instance.get_point_detail("123456")
        message = "Server gave incorrect data"
        self.assertEqual(str(context_manager.exception), message)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_server_404_error(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        with self.assertRaises(HttpException) as context_manager:
            await api_instance.get_point_detail("1234567")
        self.assertEqual(context_manager.exception.status_code, 404)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_long_name_1(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(
            api_instance.get_line_long_name("5"), "ERASME - HERRMANN-DEBROUX"
        )

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_long_name_2(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(api_instance.get_line_long_name("76"), "KRAAINEM - OPPEM")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_long_name_invalid_id(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        with self.assertRaises(ValueError) as context_manager:
            await api_instance.get_line_long_name("1234")
        message = "unknown line id"
        self.assertEqual(str(context_manager.exception), message)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_type_1(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(api_instance.get_line_type("5"), "1")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_type_2(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(api_instance.get_line_type("88"), "3")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_type_invalid_id(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        with self.assertRaises(ValueError) as context_manager:
            await api_instance.get_line_type("21234")
        message = "unknown line id"
        self.assertEqual(str(context_manager.exception), message)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_color_1(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(api_instance.get_line_color("1"), "C4008F")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_color_2(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(api_instance.get_line_color("21"), "F7E017")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_color_invalid_id(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        with self.assertRaises(ValueError) as context_manager:
            await api_instance.get_line_color("2234")
        message = "unknown line id"
        self.assertEqual(str(context_manager.exception), message)

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_text_color_1(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(api_instance.get_line_text_color("1"), "FFFFFF")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_text_color_2(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        self.assertEqual(api_instance.get_line_text_color("4"), "000000")

    @unittest_run_loop
    @asynctest.patch("src.pyodstibmivb.odstibmivb.URL", "/")
    async def test_get_line_text_color_invalid_id(self):
        api_instance = ODStibMivb(API_KEY, self.client)
        with self.assertRaises(ValueError) as context_manager:
            await api_instance.get_line_text_color("2238")
        message = "unknown line id"
        self.assertEqual(str(context_manager.exception), message)

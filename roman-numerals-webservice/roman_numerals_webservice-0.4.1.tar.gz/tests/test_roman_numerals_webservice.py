import pytest
import numpy
from roman_numerals_webservice import RomanNumeralsWebservice
from roman_numerals_webservice.roman_numerals import arabic_to_roman, roman_to_arabic

from http import HTTPStatus
import cherrypy
import requests
import json

from contextlib import contextmanager


@contextmanager
def run_server():
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()
    cherrypy.engine.block()


def roman_numer_service_runner(func):
    def func_wrapper(self):
        cherrypy.tree.mount(RomanNumeralsWebservice())
        with run_server():
            func(self)

    return func_wrapper


class TestRomanNumeralsWebservice(object):
    url_arabic_to_roman = "http://localhost:8080/arabic_to_roman"
    url_roman_to_arabic = "http://localhost:8080/roman_to_arabic"

    @roman_numer_service_runner
    def test_arabic_to_roman_valid_input(self):

        url = TestRomanNumeralsWebservice.url_arabic_to_roman

        # testing all is to slow
        for arabic in list(range(1, 4000, 17)) + [3999]:
            r = requests.post(url, json={"arabic": arabic})
            assert r.status_code == HTTPStatus.OK
            json_res = json.loads(r.json())
            assert json_res["roman"] == arabic_to_roman(arabic)

    @roman_numer_service_runner
    def test_arabic_to_roman_valid_input_advanced(self):

        url = TestRomanNumeralsWebservice.url_arabic_to_roman

        # in python bool is subclass of int
        r = requests.post(url, json={"arabic": True})
        json_res = json.loads(r.json())
        assert json_res["roman"] == arabic_to_roman(1)

    @roman_numer_service_runner
    def test_arabic_to_roman_invalid_input(self):

        url = TestRomanNumeralsWebservice.url_arabic_to_roman

        # wrong range
        r = requests.post(url, json={"arabic": 0})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"arabic": 4000})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"arabic": -1})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"arabic": False})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # wrong type
        r = requests.post(url, json={"arabic": "1"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"arabic": [1]})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # wrong key
        r = requests.post(url, json={"Arabic": 1})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"roman": 1})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={" arabic": 1})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"arabic ": 1})
        assert r.status_code == HTTPStatus.BAD_REQUEST

    @roman_numer_service_runner
    def test_araic_to_roman_valid_input(self):

        url = TestRomanNumeralsWebservice.url_roman_to_arabic

        # testing all is to slow
        for arabic in list(range(1, 4000, 17)) + [3999]:
            roman = arabic_to_roman(arabic)
            r = requests.post(url, json={"roman": roman})
            assert r.status_code == HTTPStatus.OK
            json_res = json.loads(r.json())
            assert json_res["arabic"] == arabic

        # testing all is to slow
        for arabic in list(range(1, 4000, 17)) + [3999]:
            roman = arabic_to_roman(arabic)
            r = requests.post(url, json={"roman": roman.lower()})
            assert r.status_code == HTTPStatus.OK
            json_res = json.loads(r.json())
            assert json_res["arabic"] == arabic

    @roman_numer_service_runner
    def test_araic_to_invalid_input(self):

        url = TestRomanNumeralsWebservice.url_roman_to_arabic

        # wrong whitespace
        r = requests.post(url, json={"roman": " X"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # wrong whitespace
        r = requests.post(url, json={"roman": "X "})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # wrong type
        r = requests.post(url, json={"roman": 1})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"roman": True})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"roman": ["X"]})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"roman": ("X",)})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # invalid roman numeral
        r = requests.post(url, json={"roman": "XXXX"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # not a roman numeral
        r = requests.post(url, json={"roman": "IVMCX"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # not a roman numeral
        r = requests.post(url, json={"roman": "abc"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        # wrong key
        r = requests.post(url, json={" roman": "I"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"roman ": "I"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"arabic": "I"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

        r = requests.post(url, json={"Roman5": "I"})
        assert r.status_code == HTTPStatus.BAD_REQUEST

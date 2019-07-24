# -*- coding: utf-8 -*-

"""Main module."""

import cherrypy
import json
from http import HTTPStatus

from .roman_numerals import arabic_to_roman, roman_to_arabic


class RomanNumeralsWebservice(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media="application/json")
    def roman_to_arabic(self):
        """Implements endpoint for Roman to Arabic web-service
        
        This method expects json request with a json payload of
        the following form:

        .. code-block:: python

            '{"roman": <input_str>}'

        Where :code:`<input_str>` is the input Roman numerals as string.
        The string can be in CAPTIAL lower or mIxeD case.
        
        
        With curl, one can use this endpoint in the following way:

        .. code-block:: shell
        
            $ curl -d '{"roman" : "XL"}' -H "Content-Type: application/json" -X POST http://localhost:8080/roman_to_arabic
        
        The output will be:

        .. code-block:: shell
            
            {\"arabic\": 40}"
      


        Returns:
            str: json string of the form :code:`'{"arabic": <res_int>}'` where
                :code:`<res_int>` is an integer which represents the 
                    input Roman numeral converted to an Arabic Numeral.

        
        Raises:
            cherrypy.HTTPError: If the input it not a valid Roman numeral
                or if the json payload is ill-formed, a :code:`cherrypy.HTTPError(status=400)` 
                is raised. This error will translate to a BAD_REQUEST HTML status code.
        """

        json_dict = cherrypy.request.json

        # get input
        try:
            roman = json_dict["roman"]
        except KeyError:
            raise cherrypy.HTTPError(
                status=HTTPStatus.BAD_REQUEST, message='json key "roman" is missing'
            )

        # process input
        try:
            arabic = roman_to_arabic(roman)
        except ValueError:
            raise cherrypy.HTTPError(
                status=HTTPStatus.BAD_REQUEST,
                message="input is not a canonical roman numeral",
            )
        except TypeError:
            raise cherrypy.HTTPError(
                status=HTTPStatus.BAD_REQUEST,
                message="input value needs to be a string",
            )

        # return result
        return json.dumps(dict(arabic=arabic))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media="application/json")
    def arabic_to_roman(self):
        """Implements endpoint for Arabic to Roman web-service
        
        This method expects json request with a json payload of
        the following form:

        .. code-block:: python

            '{"roman": <input_str>}'

        Where :code:`<input_str>` is the input Arabic numerals as integer.
        
        
        With curl, one can use this endpoint in the following way:

        .. code-block:: shell
        
            $ curl -d '{"arabic" : 1987}' -H "Content-Type: application/json" -X POST http://localhost:8080/arabic_to_roman
        
        The output will be:
        
        .. code-block:: shell
            
            "{\"roman\": \"MCMLXXXVII\"}"
      


        Returns:
            str: json string of the form :code:`'{"roman": <res_str>}'` where
                :code:`<res_str>` is an str which represents the 
                    input Arabic numeral converted to a Roman Numeral.

        
        Raises:
            cherrypy.HTTPError: If the input is not a in the range :code:`[1,...399]`,
                if the json payload is ill-formed, a :code:`cherrypy.HTTPError(status=400)` 
                is raised. This error will translate to a BAD_REQUEST HTML status code.
        """
        json_dict = cherrypy.request.json

        # get input
        try:
            arabic = json_dict["arabic"]
        except KeyError:
            raise cherrypy.HTTPError(
                status=HTTPStatus.BAD_REQUEST, message='json key "arabic" is missing'
            )

        # process input
        try:
            roman = arabic_to_roman(arabic)

        except TypeError:
            raise cherrypy.HTTPError(
                status=HTTPStatus.BAD_REQUEST,
                message="input value needs to be an integer",
            )
        except ValueError:
            raise cherrypy.HTTPError(
                status=HTTPStatus.BAD_REQUEST,
                message="arabic number must be between 1 and 3999",
            )

        return json.dumps(dict(roman=roman))

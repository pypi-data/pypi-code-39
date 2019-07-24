# -*- coding: utf-8 -*-

"""Main module."""

import cherrypy
import json
from http import HTTPStatus

from . roman_numerals import int_to_roman, roman_to_int




class RomanNumeralsWebservice(object):


    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media='application/json')
    def roman_to_arabic(self):

        json_dict = cherrypy.request.json

        # get input
        try:
            roman = json_dict['roman']
        except KeyError:
            raise cherrypy.HTTPError(status=HTTPStatus.BAD_REQUEST,
                message='json key "roman" is missing')

        # process input
        try:
            arabic = roman_to_int(roman)
        except ValueError:
            raise cherrypy.HTTPError(status=HTTPStatus.BAD_REQUEST, 
                message='input is not a canonical roman numeral')
        except TypeError:
            raise cherrypy.HTTPError(status=HTTPStatus.BAD_REQUEST, 
                message='input value needs to be a string')

        # return result
        return json.dumps(dict(arabic=arabic))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media='application/json')
    def arabic_to_roman(self):
        json_dict = cherrypy.request.json
        
        # get input
        try:
            arabic = json_dict['arabic']
        except KeyError:
            raise cherrypy.HTTPError(status=HTTPStatus.BAD_REQUEST,
                message='json key "arabic" is missing')

        # process input
        try:
            roman = int_to_roman(arabic)

        except TypeError:
            raise cherrypy.HTTPError(status=HTTPStatus.BAD_REQUEST, 
                message='input value needs to be an integer')
        except ValueError:
            raise cherrypy.HTTPError(status=HTTPStatus.BAD_REQUEST, 
                message='arabic number must be between 1 and 3999')

        
        return json.dumps(dict(roman=roman))




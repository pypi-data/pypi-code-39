#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
The Valispace API, version 2
"""


import getpass
import json
import requests
import sys
import re
import urllib


class Workspace:
    """
    Represents a Valispace workspace
    """
    def __init__(self) -> None:
        self.id: int = -1


class Project:
    """
    Represents a Valispace project
    """
    def __init__(self) -> None:
        self.id: int = -1


class Component:
    """
    Represents a Valispace component
    """
    def __init__(self) -> None:
        self.id: int = -1


class Vali:
    """
    Represents a Valispace vali
    """
    def __init__(self) -> None:
        self.id: int = -1
        self.shortname: str = None


class Matrix:
    """
    Represents a Valispace matrix
    """
    def __init__(self) -> None:
        self.id: int = -1


class TextVali:
    """
    Represents a Valispace textvali
    """
    def __init__(self) -> None:
        self.id: int = -1


class Valispace:
    """
    The Valispace API
    """
    def __init__(self, url: str, username: str, password: str) -> None:
        """
        Initializes a connection to the Valispace API

        Parameters
        ----------
        username : str
            The username
        password : str
            The password

        TODO: document exceptions
        """
        if url is None:
            raise ValueError("Invalid url")

        url = url.strip().rstrip("/")

        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url

        if url[:5] != "https":
            sys.stderr.write("Please use HTTPS if possible")

        self._url = url + '/rest/'
        self._oauth_url = url + '/o/token/'
        self._session = requests.Session()
        self.username, self.password = username, password
        self._login()


    def _login(self) -> None:
        """
        Performs the password-based oAuth 2.0 login for read/write access.

        Returns
        -------
        None

        """
        # clear out old auth headers
        self._session.headers = {}

        try:
            client_id = "ValispaceREST"  # registered client-id in Valispace Deployment
            response = self._session.post(self._oauth_url, data={
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
                "client_id": client_id,
            })
        except requests.exceptions.RequestException as e:
            raise Exception("VALISPACE-ERROR: " + str(e))
        except:
            # TODO:
            # T: Capture specific exceptions, bc it is also possible that
            # the endpoint does not work or something like that...
            raise Exception("VALISPACE-ERROR: Invalid credentials or url.")

        response.raise_for_status()

        json = response.json()

        if 'error' in json and json['error'] != None:
            if 'error_description' in json:
                raise Exception("VALISPACE-ERROR: " + json['error_description'])
            else:
                raise Exception("VALISPACE-ERROR: " + json['error'])
            return

        access = "Bearer " + json['access_token']
        self._session.headers = {
            'Authorization': access,
            'Content-Type': 'application/json'
        }
        return


    def _json_request(self, method: str, url: str, data: dict=None, params: dict=None) -> dict:
        if data is None:
            data = {}

        url += '?' + urllib.parse.urlencode({"a":"b"}

        return self._session.request(method, self._url + url, data=data)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class JwtClient:
    def __init__(self, uaa_client):
        self.uaa_client = uaa_client
        self.token = ""
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }

    def refetch_token(self):
        self.token = self.uaa_client.get_token()
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }

    def set_token(self, token):
        self.uaa_client.set_token(token)
        self.refetch_token()

    def get(self, url, **kwargs):
        response = requests.get(url, headers=self.headers, **kwargs)
        if response.status_code == 401:
            self.refetch_token()
            response = requests.get(url, headers=self.headers, **kwargs)
        return response.status_code, response.content

    def post(self, url, *args, **kwargs):
        response = requests.post(url, *args, headers=self.headers, **kwargs)
        if response.status_code == 401:
            self.refetch_token()
            response = requests.post(url, *args, headers=self.headers, **kwargs)
        return response.status_code, response.headers

    def put(self, url, *args, **kwargs):
        response = requests.put(url, *args, headers=self.headers, **kwargs)
        if response.status_code == 401:
            self.refetch_token()
            response = requests.put(url, *args, headers=self.headers, **kwargs)
        return response.status_code

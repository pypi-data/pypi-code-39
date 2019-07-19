# encoding: utf-8

import os

callback_url = os.getenv('JOB_UPDATE_URL', None)
job_access_token = os.getenv('JOB_ACCESS_TOKEN', None)
uaa_token_url = os.getenv('UAA_TOKEN_URL', 'http://localhost:8080/users/login')
uaa_username = os.getenv("UAA_USERNAME", "admin")
uaa_password = os.getenv("UAA_PASSWORD", "123")
import haven

from datetime import datetime
from dateutil.tz import tzutc


class AuthedApiClient(haven.ApiClient):
    def __init__(self, id, secret, configuration=None, pool_threads=1):
        super(AuthedApiClient, self).__init__(configuration=configuration, pool_threads=pool_threads)
        # We use these fields to keep our refresh tokens up to date.
        self.api = haven.DefaultApi(haven.ApiClient(configuration))
        self.token_request = haven.TenantServiceAccountAgentLoginRequest(id=id, secret=secret)
        self.token_response = None

    def _update_token(self):
        if not self.token_response or self.token_response.expiry < datetime.utcnow().replace(tzinfo=tzutc()):
            self.token_response = self.api.create_access_token(self.token_request)

    def call_api(self, resource_path, method,
                 path_params=None, query_params=None, header_params=None,
                 body=None, post_params=None, files=None,
                 response_type=None, auth_settings=None, async_req=None,
                 _return_http_data_only=None, collection_formats=None,
                 _preload_content=True, _request_timeout=None, _host=None):
        # Update the token if expired & insert it into the HTTP headers.
        self._update_token()
        headers = header_params if header_params else {}
        headers['Authorization'] = 'Bearer %s' % self.token_response.token
        # send the request
        return super(AuthedApiClient, self).call_api(
            resource_path, method, path_params, query_params, headers,
            body, post_params, files, response_type, auth_settings, async_req,
            _return_http_data_only, collection_formats, _preload_content,
            _request_timeout, _host)

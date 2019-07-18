from cuculus import CuculusClient
from cuculus import CuculusLoggingHandler


class CuculusHttpLoggingHandler(CuculusLoggingHandler):
    def __init__(self,
            collector_url: str,
            app_id: str):
        client = CuculusClient(collector_url, app_id)
        client.start()
        CuculusLoggingHandler.__init__(self, client, app_id)

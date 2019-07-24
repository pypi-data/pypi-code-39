import cnvrg.helpers.apis_helper as apis_helper
import cnvrg.helpers.param_build_helper as param_build_helper

class BaseConnector():
    def __init__(self, data_connector):
        org, data_connector = param_build_helper.parse_params(data_connector, param_build_helper.DATA_CONNECTOR)
        self._org = org
        self._data_connector = data_connector
        self.data = self.__init_data_connector()

    def __init_data_connector(self):
        return apis_helper.get(self.__base_url()).get("data_connector")

    def __base_url(self):
        return apis_helper.url_join('users', self._org, "data_connectors", self._data_connector)
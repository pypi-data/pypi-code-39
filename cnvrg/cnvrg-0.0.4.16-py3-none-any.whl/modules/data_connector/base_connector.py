import cnvrg.helpers.apis_helper as apis_helper
import cnvrg.helpers.param_build_helper as param_build_helper

class BaseConnector():
    def __init__(self, data_connector, info=None):
        org, data_connector = param_build_helper.parse_params(data_connector, param_build_helper.DATA_CONNECTOR)
        self._org = org
        self._data_connector = data_connector
        self.info = None
        self.__init_data_connector(info=info)

    def connector_type(self):
        return self.info.get("connector_type")

    def __init_data_connector(self, info=None):
        self.info = info or apis_helper.get(self.__base_url()).get("data_connector")
        self.data = self.info.get("credentials")

    def __base_url(self):
        return apis_helper.url_join('users', self._org, "data_connectors", self._data_connector)


    def torch_ds(self):
        from torch.utils.data.dataset import Dataset as TorchDataset
        class TorchDs(TorchDataset):
            def __init__(self, dc):
                self.__dc = dc
            def __getitem__(self, item):
                return self.__dc[item]
            def __len__(self):
                return len(self.__dc)
        return TorchDs(self)

    def data_loader(self, **kwargs):
        from torch.utils import data
        class DataLoader(data.DataLoader):
            def __init__(self, dc, **kwargs):
                super(DataLoader, self).__init__(dc.torch_ds(), **kwargs)
        return DataLoader(self, **kwargs)
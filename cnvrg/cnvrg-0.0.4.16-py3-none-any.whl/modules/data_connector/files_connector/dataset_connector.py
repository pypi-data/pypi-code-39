from cnvrg.modules.data_connector.base_connector import BaseConnector
from cnvrg.modules.dataset import Dataset
from cnvrg.helpers.apis_helper import url_join

class DatasetConnector(BaseConnector):

    @staticmethod
    def key_type():
        return "bucket"

    def __init__(self, dataset=None, working_dir=None):
        super(DatasetConnector, self).__init__(dataset)
        self.__files = None
        self.__dataset = Dataset(url_join(self._org, self._data_connector), working_dir=working_dir)

    #
    # def get_base_url(self):
    #     return "users/{owner}/datasets/{dataset}".format(owner=self.__owner, dataset=self.__dataset)
    #
    # def fetch_all_files(self):
    #     return self.get_commit_files()

    def __len__(self):
        if not self.__files: self.__files = self.__dataset.fetch_all_files()
        return len(self.__files)

    def __getitem__(self, item):
        return self.__dataset.download_file(self.__files[item])
from dsn.bitgrit.gcp.dataset_api import DatasetAPI
from enum import Enum


class DatasetType(Enum):
    TEXTS = 1
    IMAGES = 2
    VIDEOS = 3


class Dataset:

    def __init__(self, dataset_type, file_name, desired_file_name=''):
        self._dataset_api = DatasetAPI(dataset_type)
        self._file_name = file_name
        if desired_file_name:
            self.desired_file_name = desired_file_name
        else:
            from pathlib import Path
            self.desired_file_name = Path(file_name).name


    @property
    def file_name(self):
        return self._file_name

    @property
    def dataset_api(self):
        return self._dataset_api

    async def get_title(self):
        return await self._dataset_api.get_metadata(self.file_name, 'title')

    async def set_title(self, title):
        await self._dataset_api.set_metadata(self.file_name, {'title': title})

    async def get_subtitle(self):
        return await self._dataset_api.get_metadata(self.file_name, 'subtitle')

    async def set_subtitle(self, subtitle):
        await self._dataset_api.\
            set_metadata(self.file_name, {'subtitle': subtitle})

    async def get_description(self):
        return await self._dataset_api.\
            get_metadata(self.file_name, 'description')

    async def set_description(self, description):
        await self._dataset_api.\
            set_metadata(self.file_name, {'description': description})

    async def get_license(self):
        return await self._dataset_api.get_metadata(self.file_name, 'license')

    async def set_license_type(self, license_type):
        await self._dataset_api.\
            set_metadata(self.file_name, {'license_type': license_type})

    async def get_industry(self):
        return await self._dataset_api.get_metadata(self.file_name, 'industry')

    async def set_industry(self, industry):
        return await self._dataset_api.\
            set_metadata(self.file_name, {'industry': industry})

    async def set_metadata(self, metadata):
        return await self._dataset_api.set_metadata(self.file_name, metadata)

    async def get_complete_metadata(self):
        return await self._dataset_api.get_complete_metadata(self.file_name)

    async def upload(self):
        return await self._dataset_api.\
            upload_file(self._file_name, self.desired_file_name)

    async def download(self):
        pass

    async def delete(self):
        await self._dataset_api.delete_file(self.file_name)
        del self

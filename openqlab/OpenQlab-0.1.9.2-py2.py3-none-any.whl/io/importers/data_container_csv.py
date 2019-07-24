from OpenQlab.io.base_importer import StreamImporter
from OpenQlab.io.data_container import DataContainer
from OpenQlab.io.importers import utils


class DataContainerCSV(StreamImporter):
    NAME = 'DataContainerCSV'
    AUTOIMPORTER = True
    STARTING_LINES = ['^' + DataContainer.json_prefix]

    def read(self):
        self._check_header()
        output = DataContainer.from_csv(self._stream, parse_dates=True)
        if output.empty:
            raise utils.ImportFailed(
                    f"'{self.NAME}' importer: Did not find any valid data\
                            in file '{self._stream.name}'")
        return output


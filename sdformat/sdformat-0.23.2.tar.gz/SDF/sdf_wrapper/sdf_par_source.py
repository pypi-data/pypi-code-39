import getpass
import platform
from ..sdf_par import sdf_par
from .. import __version__


class sdf_par_source(sdf_par):

    def __init__(self):        
        super(sdf_par_source, self).__init__("source-of-sdf-file")

    def FillDefaultSystemParameters(self):
        self.SetUserName(getpass.getuser())
        self.SetComputerName(platform.uname().node)
        self.SetSDFVersion(__version__)

    def SetConverter(self, converter_name):
        self._SetProperty("converter", converter_name)

    def SetSourceFile(self, source_file_name):
        self._SetProperty("source-file", source_file_name)
        
    def SetSourceFileType(self, file_type_str):
        self._SetProperty("source-file-type", file_type_str)

    def SetUserName(self, username: str):
        self._SetProperty('user-name', username)

    def SetComputerName(self, computername: str):
        self._SetProperty('computer-name', computername)

    def SetSDFVersion(self, version: str):
        self._SetProperty('sdf-version', version)
        
    def _SetProperty(self, property_name, property_value):
        try:
            property_par = self[property_name]
            property_par.Set(property_name, property_value)
        except KeyError:
            property_par = sdf_par(property_name, property_value)
            self.AppendPar(property_par)

    

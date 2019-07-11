import pysftp
import os

class SFTP(pysftp.Connection):
    def __init__(self,
                 remote_dir='~/',
                 local_dir='./',
                 skip_verification=False,
                 *args, **kwargs):
        self.remote_dir = remote_dir
        self.local_dir = local_dir
        super().__init__(*args, **kwargs)
        self.cd(self.remote_dir)

    def get(self, remote_file, local_file, overwrite=False):
        if not self.lexists(remote_file):
            raise OSError("Remote file {} does not exist.".format(remote_file))
        if local_file[-1] == '/':
            local_file = os.path.join(
                local_file, os.path.basename(remote_file))
        if not overwrite:
            if os.path.exists(local_file):
                raise OSError(
                    "Local file {} exists, specify overwrite=True to force overwriting.".format(local_file))
        super().get(remote_file, local_file)

    def put(self, local_file, remote_path=None, overwrite=False, makedirs=False):
        """Transfer a local file to server.

        Parameters
        ==========
        makedirs : True/False
            create remote directories in the way automatically.
        """
        if remote_path is None:
            # did not specify, use default folder
            remote_path = self.remote_dir

        if self.lexists(remote_path):
            if self.isdir(remote_path):
                remote_path = os.path.join(
                    remote_path, os.path.basename(local_file))
            else:
                if self.isfile(remote_path):
                    if not overwrite:
                        raise OSError(
                            "Remote path {} exists, specify overwrite=True to force overwriting.".format(remote_path))
        if makedirs:
            dir = os.path.split(remote_path)[0]
            self.makedirs(dir, mode=777)

        return super().put(local_file, remote_path)

    def read_file(self, remote_file, func, **kwargs):
        """Read a remote file using the specified function

        Parameters
        ==========
        remote_file : string
            path on the remote server to the file
        func : function
            function to read the remote file
        **kwargs : dict
            additional parameters to pass to the reader function
        
        Returns
        ======
        result : <unknown>
            whatever the reader function returns
        """
        tmp_file = os.path.join(self.local_dir, os.path.basename(remote_file))
        self.get(remote_file, tmp_file, overwrite=True)
        r = func(tmp_file, **kwargs)
        os.remove(tmp_file)
        return r

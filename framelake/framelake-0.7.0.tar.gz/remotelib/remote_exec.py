
import getpass
import subprocess
import fabric


def snazz(code):
    if code == 0:
        return "[REX-OK]"
    else:
        return "[!FAIL!]"


class REX:

    version = "0.5.2"

    debug_level = 2
    rex_history = []

    def __init__(self, target, user=None, pass_=None, port=None, audit_file=None, silent=True):
        """
        REX: Remote EXecute: connect to server via SSH and execute one or a series of commands.
        :param target: IP address or hostname
        :param user: username - required
        :param pass_: password - leave blank if using keys
        :param port: port - default: 22
        :param audit_file: record every command to a file
        :param silent: suppress all but the most severe output
        """
        self.target = target #type: str
        self.user = user #type: str
        if user is None: self.user = getpass.getuser()
        self.pass_ = pass_ #type: str
        self.port = port #type: int
        self.silent = silent #type: bool
        if port is None: self.port = 22
        self.audit_file = audit_file #type: str or os.path
        self.conn = self._boot_conn() #type: fabric


    def _boot_conn(self) -> fabric.Connection:
        """
        Start an SSH connection
        :return: REX object
        """
        if self.pass_ is None:
            c = fabric.Connection(self.target, port=self.port, user=self.user)
        else:
            c = fabric.Connection(self.target, port=self.port, user=self.user, connect_kwargs = { "password": self.pass_ })
        c.run(" ")
        assert c.is_connected
        return c


    def _kill_conn(self):
        """
        Kill connection.
        :return:
        """
        self.conn.close()

    def _audit(self, data) -> bool:
        """
        Write STDOUT to a file.
        :param data: strin to write
        :return: True if enabled, false if not
        """
        if self.audit_file is None:
            return False
        with open(self.audit_file, "a") as d:
            d.write(data)
        return True

    def _check_conn(self) -> bool:
        """
        Check if connection is active
        :return:
        """
        if self.conn.is_connected:
            return True
        else:
            return False

    def _fp(self, data):
        """
        Prints data and flushes stdout.
        :param data:
        :return:
        """
        if self.debug_level > 0:
            print(data, flush=True, end="")
        #return data

    def check(self):
        return self._check_conn()

    def rex(self, cmd, audit=True, bg=False, logfilename="deploy1.log"):
        """
        Remote EXecute a command to the given target.
        :param cmd: command to execute remotely
        :param audit: bool; if yes, writes return to file
        :param bg: bool; if yes, suppresses the returned stdout
        :param logfilename: particular log file that you would prefer
        :return: a connection object (fabric)
        """
        if self._check_conn() is False:
            raise ConnectionError("Fail: REX connection is not currently active!")
        self.rex_history.append(cmd)
        if bg is not True:
            rexret = self.conn.run(cmd, hide=True)
        else:
            rexret = self.conn.run("nohup {} &>{} &".format(cmd, logfilename), hide=True)
        if audit is True:
            self._audit(rexret.stdout)
        self._fp(snazz(rexret.return_code))
        if self.debug_level > 1:
            self._fp(rexret.stdout)
        return rexret

    def rex_push(self, local_path, remote=None):
        """
        Poor man's SCP, takes any builtin except dict.
        :param local: local file or files to send
        :param remote: remote directory  (or filename if single)
        :return: a list of connection objects
        """
        if remote is None:
            remote_path = "/home/" + self.user
        if self._check_conn() is False:
            raise ConnectionError("Fail: REX Push attempted with dead conn!")
        pushret = []
        if type(local_path) in [int, float, str]:
            pushret.append(
                self.conn.put(local_path, remote)
            )
        if isinstance(local_path, dict):
            raise NotImplementedError("Improper format: dict! ")

        else:
            for item in local_path:
                pushret.append(
                    self.conn.put(item, remote)
            )
        return pushret

    def rex_pull(self, remote_abs_path, local_directory):
        """
        SCP but towards localhost. Remote path must (generally) be absolute
        :param remote_abs_path: Filename to pull
        :param local_directory: where to place the pulled file
        :return:
        """
        if self._check_conn() is False:
            raise ConnectionError("Fail: Attempting to pull from dead connection!")
        pullret = self.conn.get(remote_abs_path, local_directory)
        self._fp("Pull: <-- {} -- {}".format(remote_abs_path, pullret.local))
        return pullret


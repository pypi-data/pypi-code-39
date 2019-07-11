"""
SSH Tunnel:

Create an SSH tunnel with no external dependencies.

Useful as a simple gateway to execute Python commands on a remote
port. Note that this has not undergone rigorous unit testing.

Tested to work with RemoteDB on multiple different targets runing MySQL.

Currently only does local forwarding (need to fix that but
it shouldnt be too hard.

NOTE: This is probably not the right way to do this, however
it does work as a simple gateway to execute Python commands
remotely; eg, remote database calls (see RemoteDB class).
Essentially a bloated wrapper for subprocess + SSH.

"""
import atexit
import subprocess
import getpass
import threading
import shlex
import os
import time
import socket


### Universal destructor:
### Register an at-exit function to ensure garbage collection

def destroy_all():
    print("Caught exit; cleanup time. Ctrl+C will close all connections if this hangs.")
    for tun in Tunnels():
        tun.kill()
    
atexit.register(destroy_all)


class Tunnels:
    """ Container class. Holds all active tunnels. Useful for iterating
        over tunnels
    """

    tunnels = []

    def __init__(self, tunnel_object=None):
        """ if tunnel_object -> appends object to self.tunnels
        if no object. assumes iteration (better way?)  """
        self.tunnel_object = tunnel_object
        if self.tunnel_object is not None:
            self.tunnels.append(self.tunnel_object)

    def __iter__(self):
        i = 0
        while True:

            if i >= len(self.tunnels):
                i = 0
                raise StopIteration
            else:
                yield self.tunnels[i]
                i += 1



class SSHLocalTunnel(Tunnels):
    """
    Class that uses a thread to open a tunnel to target machine.
    Roughly analagous to ssh -L 4444:localhost:3306 -N
    TODO: -> allow choosing between local and remote forwarding.
    TODO: -> suppress output
    TODEFINITELYDO: get better control of the subprocess, syncronize
    using Queue? Or something.

    
    """

    killall_flag = False

    def __init__(
            self,
            target: 'target machine',
            local_port: 'port from your chair' = 4444,
            remote_port: 'remote port to pipe to'=3306,
            remote_interface: 'interface descriptor - almost always localhost unless you screwed up mysql' = "localhost",
            remote_user: 'remote username' = getpass.getuser(),
            spin: "print the spinny thing (ie if using as bg)" = False,
            foreground: "daemonize the thread? " = False,
            **conn_opts: "Additional configuration opts"
            ):
        """
        Constructor for the SSH Tunnel. Takes the expected params except the remote host is first.
        :param target: Remote host to create a tunnel to
        :param local_port: Port to map the remote port to
        :param remote_port: remote port
        :param remote_interface: useful for specific stuff; ie 0.0.0.0 vs localhost vs 127.0.0.1 very much mean something
        :param remote_user: user@
        :param spin: print the dumb spinny thing?
        :param foreground: Execute thread as non-deamon(true) or deamon(False)
        :param conn_opts: keyword arguments
        """
        super().__init__(tunnel_object=self) # register this tunnel as a memeber of the parent class.

        self.target = target #string, hostname, alias, non-cidr ip
        self.local_port = local_port #port from your point of view
        self.remote_port = remote_port #port from their point of view

        self.remote_user = remote_user #username of individual running this script
        self.remote_interface = "127.0.0.1" #ie for mysql
        self.timeout = 150 # number of seconds / 10 that we should try to connect for before givign up and nuking the thread

        self.tunnelname = "SSH Tunnel Thread" #threadname
        self.immediate = True #do we wish to immediately start the thread as soon as constructed
        self.spin = spin #### change later
        self.foregroud = foreground # Daemon type - False allows execution of commands and is therefore default.
        self.fully_initialized = False # we specifically need to wait for this flag before executing
                                       # stuff through the tunnel - since it is in a thread it is not syncrounous.

        # untested/wip - todo: see what happen when change this
        self.local_flag = True # forward to local?
        self.terminate_flag = False

        # kinda inelegant to use a comprehension here but it beats 40 kwarg if statements.
        [setattr(self, i, conn_opts[i]) for i in conn_opts.keys()]


        # Compile the command - we wanna verify it in case of any issues, even though we will break it later
        self.compiled_command = "ssh -L {}:{}:{} {}@{} -N".format(
            self.local_port,
            self.remote_interface,
            self.remote_port,
            self.remote_user,
            self.target
        )

        ### bad hack, fix later:
        if self.local_flag is False:
            self.compiled_command = "ssh -N {}@{}".format(self.remote_user, self.target)

        print(self.compiled_command)
        self.conn = None # as soon as the thread starts, can use to check successful start


        self.elapsed = 0 # time in seconds we have run in this instance
        # the thread in question
        self.tunnel_thread = threading.Thread(
            target=self._boot_tunnel,
            name = self.tunnelname,
            daemon = foreground
        )
        # start right now?
        if self.immediate is True:
            self.tunnel_thread.start()




    def spinner(self):
        """
        Shall I say, I have gone at dusk through certain narrow streets
        And watched the smoke that rises from the pipes;
        Of lonely men in shirt-sleeves, leaning out of windows ...?
        I should have been a pair of ragged claws,
        Scuttling across the floors of silent seas!
        Generator function that powers the main loop, also, it
        does the spinny thing.
        """
        t = ["-", "\\", "|", "/", "-", "\\", "|", "/"]
        i = 0
        while True:
            if not self.tunnel_thread.is_alive():
                raise StopIteration
            if i >= len(t):
                i = 0
            yield t[i]
            i += 1

    def _boot_tunnel(self):
        """
        tunnel_thread target. This is the main function and the actual tunnel itself.
        You can turn off the spinny thing by setting spin to false in the constructor
        """
        i = 0


        self.conn = subprocess.Popen(shlex.split(self.compiled_command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print("Start: tunnel to {} [PID: {} ]".format(self.target, self.conn.pid))
        while i < self.timeout * 10:
            """
            Every 0.1 seconds attempt to connect to target and start tthe tunnel.
            Since this is in the threading ur-space and then wraps a process, we absolutely must 
            ensure that either it gets a good connection, or that we kill the process, and the 
            thread, in order to avoid zombie SSH sessions.
            """
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            time.sleep(0.1)
            try:
                s.connect((self.remote_interface, self.local_port))
                i = 0
                break
            except ConnectionRefusedError:
                print("\r-- Waiting for conn [{}]".format(i), end="", flush=True)
                i += 1
        if i >= self.timeout * 10:
            print(repr(self.conn.stderr))
            raise ConnectionError("Failed: conn not accepted after {} seconds. See above.".format(i * 10))

        """ Main loop - do the spinny thing (or not if spin if False) and then wait until killed
        -TODO: ensure they killed (atexit)
        """
        self.elapsed = 0
        for spinning in self.spinner():
            ## the main loop, as a function of the generator for the spinny thing.
            time.sleep(1)
            self.elapsed += 1

            if self.pulse() is False:
                # Technically since this is the main function of the thread, this should
                # never execute and therefore something is very seriously wrong if it does.
                print("FATAL: A thread has found itself dead from inside. This should never happen. You should examine this!")
                break
            # if /proc/pid not exist thats an easy giveaway that the tunnel has failed/closed/whatever
            if not os.path.exists("/proc/{}".format(self.conn.pid)):
                print("No PID after {} seconds.".format(self.elapsed))
                break
            # killall flag - ie a poison pill for thread
            elif self.killall_flag is True:
                print("KILLED    [PID: {}]".format(self.conn.pid))
                break
            if self.terminate_flag is True:
                print("Caught instance terminate flag: for id [{}]".format(id(self)))
                break
            if self.spin:
                print("\r{} CONNECTED [PID: {}]".format(spinning, self.conn.pid), end="", flush=True)
            # while we could get away with declaring the tunnel open when the socket first connects, lets be
            # ultra paranoid here
            self.fully_initialized = True



        print("\r  CLOSED [PID: {}] [Runtime: {}s]".format(self.conn.pid, self.elapsed))
        return


    def pulse(self):
        """ Check if the thread containing the tunnel is still active. """
        return self.tunnel_thread.is_alive()

    def kill(self):
        """
            Kill the connection in several different ways. Ensure its absolute and total
            destruction. This is absolutely overkill but not a bad choice.
        """
        dead = False
        self.terminate_flag = True
        while dead is False:
            try:
                self.conn.terminate()
                
                subprocess.run(["kill -9 {}".format(self.conn.pid)], shell=True, check=True)
            finally:
                try:
                    os.kill(self.conn.pid, 0)
                    print("Process[{}] killed cleanly.".format(self.conn.pid))
                    dead = True

                except ProcessLookupError:
                    print("Process[{}] not running.".format(self.conn.pid))
                    dead = True

                
        print("Process: {} - Termination Status: {}".format(self.conn.pid, dead))

    def __del__(self):
        self.kill()
       

    def __enter__(self, *args, **kwargs):
        """
        Context tools. WIP!

        """
        if self.conn is not None:
            return self.conn
        else:
            raise TypeError("Do not have conn. No tunnel!")

    def __exit__(self, *args, **kwargs):
        """
        Exit the context, and make sure its been killed.
        """
        return self.kill()




class SimpleTunnel(Tunnels):

    def __init__(self, tunnel_target, user=getpass.getuser(), bg=True):
        self.tunnel_target = tunnel_target
        self.user = user
        self.bg = "f" if bg is True else ""
        super().__init__(tunnel_object=self)
        self.extermination_flag = False
        self.break_flag = False
        self.base_cmd = "ssh -{}N {}@{}".format(self.bg, self.user, self.tunnel_target)
        print(self.base_cmd)
        self.pid = None
        self.proc = self._start_pipe()
        #3atexit.register(self._kill_pipe)
        self.auditor_thread = threading.Thread(
            target=self._holding_pattern,
        )
        self.auditor_thread.start()


    def _start_pipe(self):
        x = subprocess.Popen([self.base_cmd], shell=True, stderr=subprocess.PIPE)
        self.pid = x.pid
        return x

    def _holding_pattern(self):
        n = 0
        while self.extermination_flag is False:
            n += 1
            time.sleep(1)
            if n % 10 == 0:
                print(".", flush=True, end="")
        self._kill_pipe()


    def _kill_pipe(self):
        try:
            self.extermination_flag = True
            self.proc.terminate()
            overkill = subprocess.run(["kill -9 {}".format(self.pid)], shell=True)
        finally:
            s = subprocess.run(["ps -q {} | grep : | wc -l".format(self.pid)], shell=True, stdout=subprocess.PIPE)
            if s.stdout.decode == "0":
                print("Good exit")
            else:
                if self.break_flag is False:
                    self.break_flag = True
                    self._kill_pipe()
                else:
                    if self.auditor_thread.is_alive():
                        print("Pipe not closed!")
                    else:
                        print("Thread dead. Pipe: ")
                        s = subprocess.run(["ps -q {} | grep : | wc -l".format(self.pid)], shell=True,
                                           stdout=subprocess.PIPE)
                        print(s.stdout.decode())
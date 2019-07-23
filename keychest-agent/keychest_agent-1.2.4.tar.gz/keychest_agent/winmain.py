from typing import Union

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

from multiprocessing import Process, freeze_support

import sys

from keychest_agent import main

register = False

class WinMain (win32serviceutil.ServiceFramework):
    _svc_name_ = "KeyChest"
    _svc_display_name_ = "KeyChest"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_requested = False
        socket.setdefaulttimeout(120)
        self.body = None    # type: Union[None,Process]

    # noinspection PyPep8Naming
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.body.terminate()
        # pid = self.body.pid
        # os.kill(pid, signal.SIGTERM)
        # self.body.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.stop_requested = True

    # noinspection PyPep8Naming
    def SvcDoRun(self):

        global register

        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        if register:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        else:
            self.body = Process(target=main.main, args=())
            self.body.daemon = False
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.body.start()
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )

            # self.timeout = 5000  # frequency seconds (timeout is in milliseconds)
            # rc = None
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

            # while rc != win32event.WAIT_OBJECT_0:
            #     # Wait for stop signal, loop on timeout
            #     rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)


if __name__ == '__main__':
    freeze_support()
    if (len(sys.argv) > 1) and ((sys.argv[1] == '--register') or (sys.argv[1] == '--run')):
        if sys.argv[1] == '--register':
            main.main()
        else:
            main.main()
        sys.exit(0)
    elif len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WinMain)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WinMain)

import serial
import serial.tools.list_ports
import os
from .MyUtil import MyUtil as util
import shutil

class WBUpload(object):

    def put(self, file_path):
        if not self._is_empty(file_path):
            try:
                port_list = list(serial.tools.list_ports.comports())
                for i in range(len(port_list)):
                    port = port_list[i]
                    if port.pid == 29987 or port.pid == 60000:
                        currentDir = os.getcwd()
                        source_file_path = file_path
                        if os.path.exists(source_file_path):
                            source_file_path = os.path.join(currentDir, source_file_path)
                        run_loop_path = os.path.join(currentDir, 'run_loop.py')
                        target_file_path = shutil.copy(source_file_path, run_loop_path)
                        util.wb_log(file_path, source_file_path, target_file_path)
                        os.system('ampy -d 2 -p {}  put {}'.format(port.device, target_file_path))
                        util.wb_log('download done!')
                        os.remove(target_file_path)
                        break
                util.wb_error_log('未发现串口！')
            except OSError as e:
                util.wb_error_log(e)
            except Exception as e:
                util.wb_error_log(e)
    
    
    def _is_empty(self, arg):
        is_empty = False
        if not arg:
            is_empty = True
            print('参数不可以为空!')
        return is_empty
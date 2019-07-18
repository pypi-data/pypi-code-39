import sys
import io
import time
import threading

def before_run():
    buffer = io.StringIO()
    old_buffer = sys.stdout
    sys.stdout = buffer
    return buffer, old_buffer


def after_run(buffer, old_buffer):
    buffer.close()
    sys.stdout = old_buffer


def stdout_thread(stdout_buffer, faketdout_buffer, callback):
    def p(seek):
        v = stdout_buffer.getvalue()
        v = v[seek:]
        v = v.replace('[0m', "")
        if v:
            faketdout_buffer.write(v)
            lines = list(filter(lambda x: x, v.strip().split("\n")))
            callback(lines)
        return seek + len(v)

    seek = 0
    while not stdout_buffer.closed:
        seek = p(seek)
        time.sleep(0.5)



def run_callable(callable, callback):
    buffer, old_buffer = before_run()
    t = threading.Thread(target=stdout_thread, args=(buffer, old_buffer, callback))
    t.start()
    exit_status = 0
    try:
        callable()
    except Exception as e:
        callback(e)
        exit_status = 1
    time.sleep(0.5)
    after_run(buffer,old_buffer)
    t.join()
    return exit_status


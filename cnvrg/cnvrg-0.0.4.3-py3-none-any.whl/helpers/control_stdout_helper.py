import sys
import io
import time
import threading
import builtins as __builtin__

def before_run():
    buffer = io.StringIO()
    olderrio = sys.stderr
    sys.stderr = err_buffer = io.StringIO()
    def printd(*args, **kwargs):
        __builtin__.oldprint(*args, **kwargs)
        if "file" in kwargs: del kwargs["file"]
        __builtin__.oldprint(*args, file=buffer, **kwargs)
    __builtin__.oldprint = __builtin__.print
    __builtin__.print = printd
    return buffer, err_buffer, olderrio


def after_run(buffer, err_buffer, errio):
    buffer.close()
    err_buffer.close()
    __builtin__.print = __builtin__.oldprint
    sys.stderr = errio


def stdout_thread(buffer, callback):
    def p(seek):
        v = buffer.getvalue()
        v = v[seek:]
        if v:
            lines = list(filter(lambda x: x, v.strip().split("\n")))
            callback(lines)
        return seek + len(v)

    seek = 0
    while not buffer.closed:
        seek = p(seek)
        time.sleep(0.5)



def run_callable(callable, callback):
    ### the idea here is to "redirect" to stdout/stderr to buffers.
    buffer, err_buffer, errio = before_run()

    ## those threads will monitor the buffer and will call the relevant
    t = threading.Thread(target=stdout_thread, args=(buffer, callback))
    terr = threading.Thread(target=stdout_thread, args=(err_buffer, lambda x: print("\n".join(map(str, x)), file=errio)))
    t.start()
    terr.start()
    exit_status = 0
    try:
        callable()
    except Exception as e:
        exit_status = 1
    except KeyboardInterrupt as e:
        exit_status = 1
    time.sleep(0.5)
    after_run(buffer, err_buffer, errio)
    t.join()
    terr.join()
    return exit_status


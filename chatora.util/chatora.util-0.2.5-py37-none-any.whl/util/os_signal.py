__all__ = (
    'signal_handler_ctx',
)

import contextlib
import signal
import typing


@contextlib.contextmanager
def signal_handler_ctx(sig_handler_map: typing.Mapping):
    original_signal_handler_map = {
        sig_num: signal.getsignal(sig_num)
        for sig_num in sig_handler_map.keys()
    }
    for sig_num, sig_handler in sig_handler_map.items():
        signal.signal(sig_num, sig_handler)
    del sig_handler_map

    try:
        yield
    except:
        raise
    finally:
        for sig_num, sig_handler in original_signal_handler_map.items():
            with contextlib.suppress(Exception):
                signal.signal(sig_num, sig_handler)
    return

# -*- coding: utf-8 -*-

from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
from subprocess import check_output

import re
import signal

crlf_pat = re.compile(r'[\r\n]+')

class PicatKernel(Kernel):
    implementation = 'Picat'
    implementation_version = '0.1'
    language = 'Picat'
    language_version = '2.6'

    language_info = {
        'name': 'Picat',
        'codemirror_mode': 'scheme',
        'mimetype': 'text/plain',
        'file_extension': '.pi'
    }

    banner = "An Jupyter kernel for Picat - version %s" % implementation_version

    def __init__(self, **kwargs):
        super(PicatKernel,self).__init__(**kwargs)
        self._start_picat()

    def _start_picat(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.picat = replwrap.REPLWrapper("picat", "Picat> ", None)
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        code = crlf_pat.sub(' ', code.strip())
        if not code:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            output = self.picat.run_command(code, timeout=None)
        except KeyboardInterrupt:
            self.picat.child.sendintr()
            interrupted = True
            self.picat._expect_prompt()
            output = self.picat.child.before
        except EOF:
            output = self.picat.child.before + 'Restarting Picat, use CRTL+D to exit'
            self._start_picat()

        if not silent:
            # Send standard output
            stream_content = {'name': 'stdout', 'text': "\r\n".join(output.splitlines()[1:])}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}

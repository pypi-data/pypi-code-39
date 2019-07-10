from .sourcemagics import SourceMagics

def load_ipython_extension(ipython):
    ipython.register_magics(SourceMagics(ipython))

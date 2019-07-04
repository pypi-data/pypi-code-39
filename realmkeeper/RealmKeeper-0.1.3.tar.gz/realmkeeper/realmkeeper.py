from .app import app

__version__ = "0.1.3"


def main():
    app.run(host='0.0.0.0', ssl_context='adhoc')

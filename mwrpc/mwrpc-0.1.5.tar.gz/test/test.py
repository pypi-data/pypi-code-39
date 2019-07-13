from mwrpc import MwrServer

server = MwrServer()


@server.func(endpoint='calc')
def add(a, b):
    return a + b


if __name__ == '__main__':
    server.run()

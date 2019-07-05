from argparse import ArgumentParser
import logging
from threading import Event

import sys

from notify_cli.notify_client import NotifyClient

logger = logging.getLogger('notify_cli')


def main():
    parser = ArgumentParser(description='Tool to subscribe to notifications from notify-server')
    parser.add_argument('server', help='Server address to connect to (ie. localhost:8080)')
    subparsers = parser.add_subparsers(dest='action')
    send_parser = subparsers.add_parser('send')
    send_parser.add_argument('event', help='Event type to send')
    send_parser.add_argument('data', help='Data to send with event')
    receive_parser = subparsers.add_parser('receive')
    receive_parser.add_argument('event', help='Event to subscribe to')
    args = parser.parse_args()

    try:
        host, port = args.server.split(':')
        port = int(port)
    except ValueError:
        parser.error('Invalid server address')
        raise SystemExit(1)

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    client = NotifyClient(host, port)

    if args.action == 'send':
        client.send(args.event, args.data)
        print('Sent: {}'.format({'event': args.event, 'data': args.data}))
    else:
        def on_event(event):
            if sys.stdout.isatty():
                logger.info('{}: {}'.format(event['event'], event['data']))
            else:
                print(event['data'], flush=True)

        client.subscribe(args.event, on_event)
        try:
            Event().wait()
        finally:
            client.unsubscribe(args.event, on_event)


if __name__ == '__main__':
    main()

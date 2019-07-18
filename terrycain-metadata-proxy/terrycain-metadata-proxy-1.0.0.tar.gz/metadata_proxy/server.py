import asyncio
import argparse
import json
import logging
import logging.handlers
from typing import Callable, Awaitable

from aiohttp import web

from .core import Core, CONFIG_FILE

try:
    import uvloop
    uvloop.install()
except ImportError:
    uvloop = None

try:
    from .version import version as __version__
except:
    __version__ = 'unknown'

logger = logging.getLogger('metadata-proxy')
routes = web.RouteTableDef()

ALLOWED_GENERAL_KEYS = (
    'ami-id', 'ami-12345678', 'ami-launch-index', 'ami-manifest-path',
    'reservation-id', 'local-hostname', 'local-ipv4', 'hostname',
    'instance-action', 'instance-id', 'instance-type',
    'profile', 'public-keys', 'registered-state'
)


@routes.get('/status')
async def status(request: web.Request) -> web.Response:
    return web.json_response({
        'version': __version__,
        'registered': request.app['core'].aws_metadata['registered-state'] != 'unregistered'
    })


@routes.post('/register')
async def register(request: web.Request) -> web.Response:
    json_data = await request.json()
    if 'server_url' not in json or 'key' not in json_data:
        logger.warning('Register endpoint hit without server_url or key in the JSON')
        return web.Response(text='bad request', status=400)

    server_url = json_data['server_url']
    key = json_data['key']
    only_if_not_registered = 'skip_if_registered' in request.query

    http_status, text = await request.app['core'].register_proxy(server_url, key, only_if_not_registered)

    return web.json_response(text=text, status=http_status)


# AWS Routes:
@routes.get('/')
async def index(request: web.Request) -> web.Response:
    resp = '1.0\n2007-01-19\n2007-03-01\n2007-08-29\n2007-10-10\n2007-12-15\n2008-02-01\n2008-09-01\n2009-04-04\n2011-01-01\n' \
           '2011-05-01\n2012-01-12\n2014-02-25\n2014-11-05\n2015-10-20\n2016-04-19\n2016-06-30\n2016-09-02\n2018-03-28\n' \
           '2018-08-17\nlatest'

    return web.Response(text=resp)


@routes.get('/{version}/')
async def metadata_version(request: web.Request) -> web.Response:
    resp = 'dynamic\nmeta-data\nuser-data'
    return web.Response(body=resp)


@routes.get('/{version}/meta-data/')
async def metadata_index(request: web.Request) -> web.Response:
    meta_data_options = [
        'ami-id', 'ami-launch-index', 'ami-manifest-path', 'block-device-mapping/', 'events/', 'hostname',
        'iam/', 'instance-action', 'instance-id', 'instance-type', 'local-hostname', 'local-ipv4', 'mac',
        'metrics/', 'network/', 'placement/', 'product-codes', 'profile', 'public-hostname', 'public-ipv4',
        'public-keys/', 'reservation-id', 'security-groups', 'services/'
    ]

    # If iam role is none, then we dont show iam/
    if not request.app['core'].iam_role:
        meta_data_options.remove('iam/')

    return web.Response(body='\n'.join(meta_data_options))


@routes.get('/{version}/meta-data/placement/availability-zone')
async def metadata_placement_availability_zone(request: web.Request) -> web.Response:
    return web.Response(body=request.app['core'].aws_metadata['availability-zone'])


@routes.get('/{version}/meta-data/iam/')
async def metadata_iam(request: web.Request) -> web.Response:
    # If we have no host role, metadata endpoint 404's you
    if not request.app['core'].iam_role:
        return web.Response(status=404)

    resp = 'info\nsecurity-credentials/'
    return web.Response(body=resp)


@routes.get('/{version}/meta-data/iam/info')
async def metadata_iam_info(request: web.Request) -> web.Response:
    if not request.app['core'].iam_role:
        return web.Response(status=404)

    resp = {
        "Code": "Success",
        "LastUpdated": request.app['core'].last_updated_config.strftime('%y-%m-%dT%H:%M:%SZ'),
        "InstanceProfileArn": request.app['core'].iam_role,
        "InstanceProfileId": "AAAAAAAAAAAAAAAAAAAAA"
    }

    # Converting to text as getting json_response to indent is more hassle
    text = json.dumps(resp, indent=2)
    return web.json_response(text=text)


@routes.get('/{version}/meta-data/iam/security-credentials/')
async def metadata_iam_security_credentials(request: web.Request) -> web.Response:
    if not request.app['core'].iam_role:
        return web.Response(status=404)

    # Get role name from ARN
    role_text = request.app['core'].iam_role.rsplit('/', 1)[1]

    return web.Response(body=role_text)


@routes.get('/{version}/meta-data/iam/security-credentials/{profile}')
async def metadata_iam_security_credentials(request: web.Request) -> web.Response:
    if not request.app['core'].iam_role:
        return web.Response(status=404)

    profile = request.match_info['profile']

    # Check profile matches the role name
    if request.app['core'].iam_role.rsplit('/', 1)[1] != profile:
        return web.Response(status=404)

    status, text = await request.app['core'].get_host_credentials()

    if status == 200:
        return web.json_response(text=text)

    return web.Response(text=text, status=status)


@routes.get('/{version}/meta-data/{item}')
async def metadata_general(request: web.Request) -> web.Response:
    item = request.match_info['item']

    if item not in ALLOWED_GENERAL_KEYS or item not in request.app['core'].aws_metadata:
        return web.Response(status=404)

    resp = request.app['core'].aws_metadata[item]
    return web.Response(body=resp)


@web.middleware
async def aws_response(request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]) -> web.Response:
    resp = await handler(request)
    resp.headers['Connection'] = 'close'
    resp.headers['Server'] = 'EC2ws'

    return resp


async def startup(app: web.Application):
    logger.debug('Starting setup')
    await app['core'].setup()
    logger.debug('Finished setup')


async def shutdown(app):
    logger.debug('Starting shutdown')
    await app['core'].close()
    logger.debug('Finished shutdown')


def run():
    # Setup Logging
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    journalctl_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)
    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(journalctl_formatter)
    logger.addHandler(stderr_handler)

    # Setup access logging
    req_logger = logging.getLogger('metadata-proxy.http')

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--log-file', type=str, default=None, help='Log file')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=logging._levelToName.values(), help='Log level')
    parser.add_argument('--config-file', type=str, default=CONFIG_FILE, help='Config file')

    args = parser.parse_args()

    # Setup log file
    if args.log_file:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            args.log_file, when='midnight', backupCount=7, utc=True)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.setLevel(args.log_level)

    logger.debug('Initialising web application')
    app = web.Application(middlewares=[aws_response])

    app['core'] = Core()
    app.add_routes(routes)
    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)
    try:
        logger.info('Running AWS metadata server on {0}:{1}'.format(args.host, args.port))
        web.run_app(app, host=args.host, port=args.port, print=lambda x: None,
                    access_log=req_logger)
    except asyncio.CancelledError:
        pass
    logger.info('Exiting')


if __name__ == '__main__':
    run()

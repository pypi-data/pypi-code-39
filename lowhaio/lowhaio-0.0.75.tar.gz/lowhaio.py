import asyncio
import contextlib
import ipaddress
import urllib.parse
import ssl
import socket

from aiodnsresolver import (
    TYPES,
    DnsError,
    Resolver,
)


class HttpError(Exception):
    pass


class HttpConnectionError(HttpError):
    pass


class HttpDnsError(HttpConnectionError):
    pass


class HttpTlsError(HttpConnectionError):
    pass


class HttpDataError(HttpError):
    pass


class HttpConnectionClosedError(HttpDataError):
    pass


async def empty_async_iterator():
    while False:
        yield


get_current_task = \
    asyncio.current_task if hasattr(asyncio, 'current_task') else \
    asyncio.Task.current_task


def streamed(data):
    async def _streamed():
        yield data
    return _streamed


async def buffered(data):
    return b''.join([chunk async for chunk in data])


def identity_or_chunked_handler(transfer_encoding):
    return {
        b'chunked': chunked_handler,
        b'identity': identity_handler,
    }[transfer_encoding]


def get_nonblocking_sock():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    sock.setblocking(False)
    return sock


def set_tcp_cork(sock):
    sock.setsockopt(socket.SOL_TCP, socket.TCP_CORK, 1)  # pylint: disable=no-member


def unset_tcp_cork(sock):
    sock.setsockopt(socket.SOL_TCP, socket.TCP_CORK, 0)  # pylint: disable=no-member


def Pool(
        get_dns_resolver=Resolver,
        get_sock=get_nonblocking_sock,
        get_ssl_context=ssl.create_default_context,
        transfer_encoding_handler=identity_or_chunked_handler,
        sock_pre_message=set_tcp_cork if hasattr(socket, 'TCP_CORK') else lambda _: None,
        sock_post_message=unset_tcp_cork if hasattr(socket, 'TCP_CORK') else lambda _: None,
        http_version=b'HTTP/1.1',
        keep_alive_timeout=15,
        recv_bufsize=16384,
        socket_timeout=10,
):

    loop = \
        asyncio.get_running_loop() if hasattr(asyncio, 'get_running_loop') else \
        asyncio.get_event_loop()
    ssl_context = get_ssl_context()
    dns_resolve, dns_resolver_clear_cache = get_dns_resolver()

    pool = {}

    async def request(method, url, params=(), headers=(),
                      body=empty_async_iterator, body_args=(), body_kwargs=()):
        parsed_url = urllib.parse.urlsplit(url)

        try:
            ip_addresses = (ipaddress.ip_address(parsed_url.hostname),)
        except ValueError:
            try:
                ip_addresses = await dns_resolve(parsed_url.hostname, TYPES.A)
            except DnsError as exception:
                raise HttpDnsError() from exception

        key = (parsed_url.scheme, parsed_url.netloc)

        sock = get_from_pool(key, ip_addresses)

        if sock is None:
            sock = get_sock()
            try:
                await connect(sock, parsed_url, str(ip_addresses[0]))
            except Exception as exception:
                sock.close()
                raise HttpConnectionError() from exception
            except BaseException:
                sock.close()
                raise

            try:
                if parsed_url.scheme == 'https':
                    sock = tls_wrapped(sock, parsed_url.hostname)
                    await tls_complete_handshake(loop, sock, socket_timeout)
            except Exception as exception:
                sock.close()
                raise HttpTlsError() from exception
            except BaseException:
                sock.close()
                raise

        try:
            sock_pre_message(sock)
            await send_header(sock, method, parsed_url, params, headers)
            await send_body(sock, body, body_args, body_kwargs)
            sock_post_message(sock)

            code, response_headers, body_handler, unprocessed, connection = await recv_header(sock)
            response_body = response_body_generator(sock, socket_timeout, body_handler,
                                                    method, response_headers, unprocessed,
                                                    key, connection)
        except Exception as exception:
            sock.close()
            raise HttpDataError() from exception
        except BaseException:
            sock.close()
            raise

        return code, response_headers, response_body

    def get_from_pool(key, ip_addresses):
        try:
            socks = pool[key]
        except KeyError:
            return None

        while socks:
            _sock, close_callback = next(iter(socks.items()))
            close_callback.cancel()
            del socks[_sock]

            connected_ip = ipaddress.ip_address(_sock.getpeername()[0])
            if connected_ip not in ip_addresses:
                _sock.close()
                continue

            if _sock.fileno() != -1:
                return _sock

        del pool[key]

    def add_to_pool(key, sock):
        try:
            key_pool = pool[key]
        except KeyError:
            key_pool = {}
            pool[key] = key_pool

        key_pool[sock] = loop.call_later(keep_alive_timeout, close_by_keep_alive_timeout,
                                         key, sock)

    def close_by_keep_alive_timeout(key, sock):
        sock.close()
        del pool[key][sock]
        if not pool[key]:
            del pool[key]

    async def connect(sock, parsed_url, ip_address):
        scheme = parsed_url.scheme
        _, _, port_specified = parsed_url.netloc.partition(':')
        port = \
            port_specified if port_specified != '' else \
            443 if scheme == 'https' else \
            80
        address = (ip_address, port)
        await loop.sock_connect(sock, address)

    def tls_wrapped(sock, host):
        return ssl_context.wrap_socket(sock, server_hostname=host, do_handshake_on_connect=False)

    async def send_header(sock, method, parsed_url, params, headers):
        outgoing_qs = urllib.parse.urlencode(params, doseq=True).encode()
        outgoing_path = urllib.parse.quote(parsed_url.path).encode()
        outgoing_path_qs = outgoing_path + \
            ((b'?' + outgoing_qs) if outgoing_qs != b'' else b'')
        host_specified = any(True for key, value in headers if key == b'host')
        headers_with_host = \
            headers if host_specified else \
            ((b'host', parsed_url.hostname.encode('idna')),) + headers
        await send_all(loop, sock, socket_timeout, b'%s %s %s\r\n%s\r\n' % (
            method, outgoing_path_qs, http_version, b''.join(
                b'%s:%s\r\n' % (key, value)
                for (key, value) in headers_with_host
            )
        ))

    async def recv_header(sock):
        unprocessed = b''
        while True:
            unprocessed += await recv(loop, sock, socket_timeout, recv_bufsize)
            try:
                header_end = unprocessed.index(b'\r\n\r\n')
            except ValueError:
                continue
            else:
                break

        header_bytes, unprocessed = unprocessed[:header_end], unprocessed[header_end + 4:]
        lines = header_bytes.split(b'\r\n')
        code = lines[0][9:12]
        version = lines[0][5:8]
        response_headers = tuple(
            (key.strip().lower(), value.strip())
            for line in lines[1:]
            for (key, _, value) in (line.partition(b':'),)
        )
        headers_dict = dict(response_headers)
        transfer_encoding = headers_dict.get(b'transfer-encoding', b'identity')
        connection = \
            b'close' if keep_alive_timeout == 0 else \
            headers_dict.get(b'connection', b'keep-alive').lower() if version == b'1.1' else \
            headers_dict.get(b'connection', b'close').lower()
        body_handler = transfer_encoding_handler(transfer_encoding)

        return code, response_headers, body_handler, unprocessed, connection

    async def send_body(sock, body, body_args, body_kwargs):
        async for chunk in body(*body_args, **dict(body_kwargs)):
            await send_all(loop, sock, socket_timeout, chunk)

    async def response_body_generator(sock, socket_timeout, body_handler, method, response_headers,
                                      unprocessed, key, connection):
        try:
            generator = body_handler(loop, sock, socket_timeout, recv_bufsize,
                                     method, response_headers, unprocessed)
            unprocessed = None  # So can be garbage collected

            async for chunk in generator:
                yield chunk
        except BaseException:
            sock.close()
            raise
        else:
            if connection == b'keep-alive':
                add_to_pool(key, sock)
            else:
                sock.close()

    async def close():
        await dns_resolver_clear_cache()
        for socks in pool.values():
            for sock, close_callback in socks.items():
                close_callback.cancel()
                sock.close()
        pool.clear()

    return request, close


def identity_handler(loop, sock, socket_timeout, recv_bufsize,
                     method, response_headers, unprocessed):
    response_headers_dict = dict(response_headers)
    body_length = \
        0 if method == b'HEAD' else \
        None if b'content-length' not in response_headers_dict else \
        int(response_headers_dict[b'content-length'])
    return \
        identity_handler_known_body_length(
            loop, sock, socket_timeout, recv_bufsize, body_length, unprocessed) \
        if body_length is not None else \
        identity_handler_unknown_body_length(loop, sock, socket_timeout, recv_bufsize, unprocessed)


async def identity_handler_known_body_length(
        loop, sock, socket_timeout, recv_bufsize, body_length, unprocessed):
    total_remaining = body_length

    if unprocessed and total_remaining:
        total_remaining -= len(unprocessed)
        yield unprocessed

    while total_remaining:
        unprocessed = None  # So can be garbage collected
        unprocessed = await recv(loop, sock, socket_timeout, min(recv_bufsize, total_remaining))
        total_remaining -= len(unprocessed)
        yield unprocessed


async def identity_handler_unknown_body_length(
        loop, sock, socket_timeout, recv_bufsize, unprocessed):
    if unprocessed:
        yield unprocessed

    unprocessed = None  # So can be garbage collected

    try:
        while True:
            yield await recv(loop, sock, socket_timeout, recv_bufsize)
    except HttpConnectionClosedError:
        pass


async def chunked_handler(loop, sock, socket_timeout, recv_bufsize, _, __, unprocessed):
    while True:
        # Fetch until have chunk header
        while b'\r\n' not in unprocessed:
            unprocessed += await recv(loop, sock, socket_timeout, recv_bufsize)

        # Find chunk length
        chunk_header_end = unprocessed.index(b'\r\n')
        chunk_header_hex = unprocessed[:chunk_header_end]
        chunk_length = int(chunk_header_hex, 16)

        # End of body signalled by a 0-length chunk
        if chunk_length == 0:
            while b'\r\n\r\n' not in unprocessed:
                unprocessed += await recv(loop, sock, socket_timeout, recv_bufsize)
            break

        # Remove chunk header
        unprocessed = unprocessed[chunk_header_end + 2:]

        # Yield whatever amount of chunk we have already, which
        # might be nothing
        chunk_remaining = chunk_length
        in_chunk, unprocessed = \
            unprocessed[:chunk_remaining], unprocessed[chunk_remaining:]
        if in_chunk:
            yield in_chunk
        chunk_remaining -= len(in_chunk)

        # Fetch and yield rest of chunk
        while chunk_remaining:
            unprocessed += await recv(loop, sock, socket_timeout, recv_bufsize)
            in_chunk, unprocessed = \
                unprocessed[:chunk_remaining], unprocessed[chunk_remaining:]
            chunk_remaining -= len(in_chunk)
            yield in_chunk

        # Fetch until have chunk footer, and remove
        while len(unprocessed) < 2:
            unprocessed += await recv(loop, sock, socket_timeout, recv_bufsize)
        unprocessed = unprocessed[2:]


async def send_all(loop, sock, socket_timeout, data):
    try:
        latest_num_bytes = sock.send(data)
    except (BlockingIOError, ssl.SSLWantWriteError):
        latest_num_bytes = 0
    else:
        if latest_num_bytes == 0:
            raise HttpConnectionClosedError()

    if latest_num_bytes == len(data):
        return

    total_num_bytes = latest_num_bytes

    def writer():
        nonlocal total_num_bytes
        try:
            latest_num_bytes = sock.send(data_memoryview[total_num_bytes:])
        except (BlockingIOError, ssl.SSLWantWriteError):
            pass
        except BaseException as exception:
            loop.remove_writer(fileno)
            if not result.done():
                result.set_exception(exception)
        else:
            total_num_bytes += latest_num_bytes
            if latest_num_bytes == 0 and not result.done():
                loop.remove_writer(fileno)
                result.set_exception(HttpConnectionClosedError())
            elif total_num_bytes == len(data) and not result.done():
                loop.remove_writer(fileno)
                result.set_result(None)
            else:
                reset_timeout()

    result = asyncio.Future()
    fileno = sock.fileno()
    loop.add_writer(fileno, writer)
    data_memoryview = memoryview(data)

    try:
        with timeout(loop, socket_timeout) as reset_timeout:
            return await result
    finally:
        loop.remove_writer(fileno)


async def recv(loop, sock, socket_timeout, recv_bufsize):
    incoming = await _recv(loop, sock, socket_timeout, recv_bufsize)
    if not incoming:
        raise HttpConnectionClosedError()
    return incoming


async def _recv(loop, sock, socket_timeout, recv_bufsize):
    try:
        return sock.recv(recv_bufsize)
    except (BlockingIOError, ssl.SSLWantReadError):
        pass

    def reader():
        try:
            chunk = sock.recv(recv_bufsize)
        except (BlockingIOError, ssl.SSLWantReadError):
            pass
        except BaseException as exception:
            loop.remove_reader(fileno)
            if not result.done():
                result.set_exception(exception)
        else:
            loop.remove_reader(fileno)
            if not result.done():
                result.set_result(chunk)

    result = asyncio.Future()
    fileno = sock.fileno()
    loop.add_reader(fileno, reader)

    try:
        with timeout(loop, socket_timeout):
            return await result
    finally:
        loop.remove_reader(fileno)


async def tls_complete_handshake(loop, ssl_sock, socket_timeout):
    try:
        return ssl_sock.do_handshake()
    except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
        pass

    def handshake():
        try:
            ssl_sock.do_handshake()
        except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
            reset_timeout()
        except BaseException as exception:
            loop.remove_reader(fileno)
            loop.remove_writer(fileno)
            if not done.done():
                done.set_exception(exception)
        else:
            loop.remove_reader(fileno)
            loop.remove_writer(fileno)
            if not done.done():
                done.set_result(None)

    done = asyncio.Future()
    fileno = ssl_sock.fileno()
    loop.add_reader(fileno, handshake)
    loop.add_writer(fileno, handshake)

    try:
        with timeout(loop, socket_timeout) as reset_timeout:
            return await done
    finally:
        loop.remove_reader(fileno)
        loop.remove_writer(fileno)


@contextlib.contextmanager
def timeout(loop, max_time):

    cancelling_due_to_timeout = False
    current_task = get_current_task()

    def cancel():
        nonlocal cancelling_due_to_timeout
        cancelling_due_to_timeout = True
        current_task.cancel()

    def reset():
        nonlocal handle
        handle.cancel()
        handle = loop.call_later(max_time, cancel)

    handle = loop.call_later(max_time, cancel)

    try:
        yield reset
    except asyncio.CancelledError:
        if cancelling_due_to_timeout:
            raise asyncio.TimeoutError()
        raise
    finally:
        handle.cancel()

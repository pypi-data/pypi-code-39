import inspect

__all__ = ['rpc', 'exported', 'rpc_serve', 'rpc_stop']

def rpc(name=None):
    def rpc_decorator(klass):
        klass.__rpc_options = {
            'name': name if name else klass.__name__,
        }
        return klass
    return rpc_decorator

def exported(method):
    method.__rpc_export = True
    return method

def ensure_rpc_services(transporter):
    services = getattr(transporter, '__rpc_services', None)
    if services:
        return services

    services = {}
    transporter.__rpc_services = services

    async def on_rpc_call(data):
        service = services.get(data['ns'])
        if not service:
            em = transporter.emit('__rpc_return__', {
                'ns': data['ns'],
                'seq': data['seq'],
                'error': f'Service {data["ns"]} not found'
            })
            if inspect.isawaitable(em):
                await em
        method = getattr(service, data['method'], None)
        if not method or not getattr(method, '__rpc_export', False):
            em = transporter.emit('__rpc_return__', {
                'ns': data['ns'],
                'seq': data['seq'],
                'error': f'Rpc method {data["method"]} not found'
            })
            if inspect.isawaitable(em):
                await em

        try:
            value = method(*data['params'])
            if inspect.isawaitable(value):
                value = await value
            em = transporter.emit('__rpc_return__', {
                'ns': data['ns'],
                'seq': data['seq'],
                'value': value
            })
            if inspect.isawaitable(em):
                await em
        except Exception as e:
            em = transporter.emit('__rpc_return__', {
                'ns': data['ns'],
                'seq': data['seq'],
                'error': str(e)
            })
            if inspect.isawaitable(em):
                await em

    transporter.on('__rpc_call__', on_rpc_call)
    return services

def rpc_serve(transporter, service):
    options = getattr(service, '__rpc_options', None)
    if not options:
        raise Exception('Not a valid rpc service')
    services = ensure_rpc_services(transporter)
    services[options['name']] = service

def rpc_stop(transporter, service_name):
    services = getattr(transporter, '__rpc_services', None)
    if not services:
        return
    if service_name in services:
        del services[service_name]

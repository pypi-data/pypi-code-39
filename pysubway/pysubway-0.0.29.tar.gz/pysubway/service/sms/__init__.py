try:
    from service.sms import zhutong
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.sms import zhutong
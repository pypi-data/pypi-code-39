import requests


def notify_telegram(system_name, name, desc, trb):
    data = {
        'system_name': system_name,
        'name': name,
        'desc': desc,
        'trb': trb
    }
    url = 'https://2lme7p5k92.execute-api.eu-west-2.amazonaws.com/em_notifier/listener'
    try:
        _ = requests.post(url, json=data)
    except ConnectionError:
        pass


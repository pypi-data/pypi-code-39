from auger.api.cloud.rest_api import RestApi


ORGANIZATIONS = {
    'meta': {
        'status': 200,
        'pagination':
            {'limit': 100, 'total': 1, 'count': 1, 'offset': 0}
    },
    'data': [{'name': 'auger'}]
}

PROJECTS = {
    'meta': {
        'status': 200,
        'pagination': {
            'count': 2, 'limit': 100, 'offset': 0, 'total': 2}},
    'data': [
        {"id": 2, "name": "project_1",},
        {"id": 1, "name": "test_project",}]
}


def interceptor(payload, monkeypatch):
    def payloader(x, method, *args, **kwargs):
        return payload[method]
    monkeypatch.setattr(
        RestApi, 'call_ex', payloader)


def object_status_chain(statuses, monkeypatch):
    current = statuses.pop(0)
    if len(statuses):
        monkeypatch.setattr(
            RestApi, 'wait_for_object_status', lambda x, *a, **kw: current)
    return current

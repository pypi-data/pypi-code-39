import requests


def expand(url: str) -> str:
    """
    Expands shortened urls, otherwise returns same url. Raises requests exceptions if any.

    :param url: shortened url
    :return: expanded url
    """
    r = requests.get(url)
    return r.url

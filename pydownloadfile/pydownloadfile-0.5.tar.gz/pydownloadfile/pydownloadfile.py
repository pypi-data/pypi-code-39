#!/usr/bin/env python3

from requests import get
from typing import Any, Dict, Optional

from pathlib import Path

type_none_or_dict = Optional[Dict[Any, Any]]


def download_file(
    url: str,
    filepath: Path = Path(),
    headers: type_none_or_dict = None,
    proxies: type_none_or_dict = None
        ) -> None:
    """
    Download a file using requests.
    :param url: str:
        Url of the file to be downloaded.
    :param filepath: Path:
        File name to be written. (Default value = Path())
    :param headers: type_none_or_dict:
        Requests's headers. (Default value = None)
    :param proxies: type_none_or_dict:
        Requests's proxies (Default value = None)

    """
    # If filepath is not provided it will be derived from url.
    if filepath == Path():
        filepath = Path(Path(url).name)

    if filepath.is_dir():
        filepath /= Path(url).name

    filepath.write_bytes(
        get(
            url=url,
            headers=headers,
            proxies=proxies
            ).content
        )
    return None

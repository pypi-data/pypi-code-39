"""Model utilities."""
import os

import math
import requests
import torch
from pip._vendor.appdirs import user_cache_dir

from tqdm import tqdm
from citextract import project_settings


def load_model_params(model, model_name, model_uri, ignore_cache=False, device=None):
    """Load model parameters from disk or from the web.

    Parameters
    ----------
    model : torch.nn.modules.container.Sequential
        The model instance to load the parameters for.
    model_name : str
        The name of the model which should be loaded.
    model_uri : str
        Part of the URL or full URL to the model parameters. If not specified, then the latest version is pulled from
        the internet.
    ignore_cache : bool
        When true, all caches are ignored and the model parameters are forcefully downloaded.
    device : torch.device
        The device to use.

    Returns
    -------
    torch.nn.modules.container.Sequential
        The loaded PyTorch model instance.

    Raises
    ------
    ValueError
        When the model name is not supported.
    """
    model_names = ['refxtract', 'titlextract']
    if model_name not in model_names:
        raise ValueError('The model name should be one of the following: {}.'.format(str(model_names)))
    base_url = "https://github.com/kmjjacobs/citextract-models/blob/master/" + model_name + "/"
    cache_path = os.path.join(user_cache_dir('citextract'), 'models')
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    path = os.path.join(cache_path, model_name + '-' + project_settings.get(model_name + '_version') + '.torch')
    if not os.path.exists(path) or ignore_cache:
        url = base_url + model_name + "-" + project_settings.get(model_name + '_version') + ".torch?raw=true"
        if model_uri:
            if '://' in model_uri:
                url = model_uri
            else:
                url = base_url + model_uri
                url = url + ".torch" if ".torch" not in model_uri else url
                url += "?raw=true"
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        wrote = 0
        with open(path, 'wb') as out_file:
            for data in tqdm(response.iter_content(1024), total=math.ceil(total_size // 1024), unit='KB',
                             unit_scale=True):
                wrote = wrote + len(data)
                out_file.write(data)
        if 0 < total_size != wrote:
            raise ValueError('Error downloading the model parameters from URL "' + url + '".')
    model.load_state_dict(torch.load(path), strict=False)
    model.eval()
    return model.to(device)

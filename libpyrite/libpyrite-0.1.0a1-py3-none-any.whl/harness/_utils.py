from tqdm import tnrange, trange, tqdm, tqdm_notebook


def get_tqdm_aliases(notebook_mode):
    if notebook_mode:
        _tqdm = tqdm_notebook
        _trange = tnrange
    else:
        _tqdm = tqdm
        _trange = trange

    return _tqdm, _trange


__all__ = ["get_tqdm_aliases"]

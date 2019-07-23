from typing import Dict, Union, Any
from sqlalchemy.ext.declarative import DeclarativeMeta
from ..exceptions import DatabaseUriNotFound


def update_flat_config_object(config, **kwargs):
    for k in kwargs:
        if hasattr(config, k):
            setattr(config, k, kwargs.get(k))


def database_uri_from_dictionary(config: Dict[str, Any],
                                 prefix: str,
                                 base: Union[DeclarativeMeta, str] = None,
                                 prefix_base_separator: str = ':',
                                 config_key_name: str = 'databases'):
    db_uri = None
    base_name = base.__name__ if type(base) is DeclarativeMeta else base
    uri_key = f'{prefix}{prefix_base_separator}{base_name}' if base else prefix
    db_uris = config.get(config_key_name, None)
    if db_uris:
        db_uri = db_uris.get(uri_key, None)
    if db_uri:
        return db_uri
    raise DatabaseUriNotFound(f'Database URI with key `config->{config_key_name}->{uri_key}` not found in provided config.')

# def load_relative(filename: str = 'config.yml', path: str = '.'):
#     conf_path = Path(sys.argv[0]).parents[len(path)]
#     # curr_path = path.dirname(path.abspath(__file__))
#     # project_path = path.dirname(app_path)
#     config_file_path = path.join(conf_path, filename)
#     config = load_config(config_file_path)
#     return config



import yaml
from pathlib import Path

class ConfigError(Exception):
    pass


class ClassdataStrMixin:
    def __str__(self):
        return '\n'.join(self._get_str_lines())

    def _get_dict_for_str(self):
        return self.__dict__

    def _get_str_lines(self, indent=0):
        for k, v in self._get_dict_for_str().items():
            get_child = getattr(v, '_get_str_lines', None)
            if get_child:
                yield '{}{}:'.format(' '*indent, k)
                yield from get_child(indent+2)
            else:
                yield '{}{}: {!r}'.format(' '*indent, k, v)


class CfgDict(dict, ClassdataStrMixin):
    def _get_dict_for_str(self):
        return self


def cfg_get(data, key, parent=None, optional=False):
    """Get an entry from the config data

    Parameters:
    data    dictionary from which to get an entry
    key     name of the entry to get
    parent  optional parent key
    """
    try:
        return data[key]
    except KeyError:
        if optional:
            return None
        full_key = '.'.join((parent, key)) if parent else key
        raise ConfigError("Missing key: {!r}".format(full_key))


def cfg_get_path(data, key, cfgpath, parent=None):
    """Get a path entry from the config data

    Parameters:
    data    dictionary from which to get an entry
    key     name of the entry to get
    cfgpath absolute path of the config file being loaded
    parent  optional parent key
    """
    p = Path(cfg_get(data, key, parent))

    if not p.is_absolute():
        # If the path is relative, it is taken relative to the
        # directory containing the config file
        p = cfgpath.parent / p

    return p.resolve()



class GssapiLdapAuthConfig(ClassdataStrMixin):
    def __init__(self, data, cfgpath, parent):
        self.mode = 'gssapi'
        self.username = cfg_get(data, 'krb_username', parent)
        self.keytab   = cfg_get_path(data, 'krb_keytab', cfgpath, parent)
        self.cache    = cfg_get_path(data, 'krb_cache', cfgpath, parent)


def LdapAuthConfig(data, cfgpath, parent):
    mode = cfg_get(data, 'mode', parent)

    cls = {
        'gssapi': GssapiLdapAuthConfig,
    }.get(mode)

    if not cls:
        raise ConfigError("Unrecognized {}: {}".format(
            '.'.join((parent, 'mode')), mode))
    return cls(data, cfgpath, parent)


class UpnSuffixConfig(ClassdataStrMixin):
    def __init__(self, data, parent):
        self.scope = 'subtree'

        if isinstance(data, str):
            self.suffix = data
        elif isinstance(data, dict):
            self.suffix = cfg_get(data, 'suffix', parent)
            self.scope = data.get('scope') or self.scope
        else:
            raise ConfigError("Invalid type {}: {}".format(parent, type(data)))

        if not self.scope in ('subtree', 'one'):
            raise ConfigError("Invalid {}: {}".format(
                '.'.join((parent, 'scope')), self.scope))


class Config(ClassdataStrMixin):
    def __init__(self, path, data):
        cfgpath = Path(path).resolve(strict=True)

        self.domain = cfg_get(data, 'domain')

        self.uid_range = self._load_range(data, 'uid_range')
        self.gid_range = self._load_range(data, 'gid_range')

        self.ldap_auth = LdapAuthConfig(cfg_get(data, 'ldap_auth'), cfgpath, 'ldap_auth')

        upn_data = cfg_get(data, 'upn_suffixes', optional=True) or {}
        self.upn_suffixes = CfgDict({
            container: UpnSuffixConfig(d, container+': upn_suffixes')
            for container, d in upn_data.items()
        })


    def _load_range(self, data, key):
        r = cfg_get(data, key)
        return range(
                cfg_get(r, 'min', key),
                cfg_get(r, 'max', key),
                )


    @classmethod
    def load(cls, path):
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
        except IOError as e:
            raise ConfigError(e)
            raise ConfigError('Error opening {}: {}'.format(path, e))
        except yaml.YAMLError as e:
            raise ConfigError(e)
            raise ConfigError('Error loading {}: {}'.format(path, e))

        return cls(path, data)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('config')
    args = ap.parse_args()

    cfg = Config.load(args.config)
    print(cfg)

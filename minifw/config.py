import os
from minifw import config_default


class Dict(dict):
    def __init__(self, names=(), values=(), **kwargs):
        super().__init__(**kwargs)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('Dict object has no attribute {}'.format(key))

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, override):
    r = dict()
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def to_dict(d):
    obj = Dict()
    for k, v in d.items():
        obj[k] = to_dict(v) if isinstance(v, dict) else v
    return obj

configs = config_default.configs
project_dir = os.path.split(os.getcwd())

try:
    my_module = __import__('{}.config_override'.format(project_dir[1]), globals(), locals(), ['configs'])
except ImportError:
    print('import error')
    pass
else:
    configs = merge(configs, my_module.configs)

configs = to_dict(configs)

__all__ = (configs, )
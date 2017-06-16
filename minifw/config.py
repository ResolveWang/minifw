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
                print(r[k])
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

try:
    from minifw import config_override
except ImportError:
    pass
else:
    configs = merge(configs, config_override.configs)

configs = to_dict(configs)

__all__ = (configs, )
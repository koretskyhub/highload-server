import os
import re

__all__ = (
    'Config'
)

_params_scheme = {
    'cpu_limit' : {
        'pattern' : re.compile(r'^cpu_limit\s+(?P<cpu_limit>\d+)$', re.M),
        'type'    : int,
        'default' : 1
    },
    'document_root' : {
        'pattern' : re.compile(r'^document_root\s+(?P<document_root>[^\s]+)$', re.M),
        'type'    : str,
    },
    'port' : {
        'pattern' : re.compile(r'^port\s+(?P<port>\d+)$', re.M),
        'type'    : int,
        'default' : 80
    },
    'host' : {
        'pattern' : re.compile(r'^host\s+(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', re.M),
        'type'    : str,
        'default' : '0.0.0.0'
    },
}

class Config:
    def __init__(self, config_path):
        self._config_path = config_path
        self.params = dict()
        self._parse()

    def _parse(self):
        if not(os.path.exists(self._config_path)):  raise ValueError('file does not exist')
        if os.path.getsize(self._config_path) == 0: raise ValueError('file is empty')

        with open(self._config_path, 'r') as file:
            data = file.read()

            for param_key in _params_scheme:
                param = _params_scheme[param_key]
                match = param['pattern'].search(data)
                if match:
                    self.params[param_key] = match.group(param_key)
                    try:
                        # преобразуем строку к типу параметра
                        if param['type'] != str:
                            self.params[param_key] = param['type'](self.params[param_key])
                    except ValueError:
                        raise ValueError('param(' + param_key + ') wrong value type')
                else:
                    if 'default' in _params_scheme[param_key].keys():
                        print('Parameter: "' + param_key +
                              '" not found in config file, using default value'
                             )
                        self.params[param_key] = _params_scheme[param_key].get('default')
                    else:
                        raise ValueError('param(' + param_key + ') missed')

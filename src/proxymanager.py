import re


class Proxy(object):
    def __init__(self, ip=None, port=None):
        if ip is not None:
            self.ip = ip
        if port is not None:
            self.port = port

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self.check_ip(value)
        if not re.match(
                r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))',
                value):
            raise ValueError('%s format wrong!' % value)
        self._ip = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self.check_port(value)
        self._port = value

    def __eq__(self, other):
        self.check_proxy(other)
        return self.ip == other.ip and self.port == other.port

    def __ne__(self, other):
        self.check_proxy(other)
        return self.ip != other.ip or self.port != other.port

    def check_ip(self, value):
        if not isinstance(value, str):
            raise ValueError('ip must be str')

    def check_port(self, value):
        if not isinstance(value, int):
            raise ValueError('port must be int', type(value))
        if value < 1 or value > 65535:
            raise ValueError('port must be 1~65535', value)

    def check_proxy(self, value):
        if not isinstance(value, Proxy):
            raise ValueError('Type error!Actual {},excepted {}'.format(type(value), type(Proxy)))

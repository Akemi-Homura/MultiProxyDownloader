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
        ProxyPool.check_proxy(other)
        return self.ip == other.ip and self.port == other.port

    def check_ip(self, value):
        if not isinstance(value, str):
            raise ValueError('ip must be str')

    def check_port(self, value):
        if not isinstance(value, int):
            raise ValueError('port must be int', type(value))
        if value < 1 or value > 65535:
            raise ValueError('port must be 1~65535', value)


class ProxyPool(object):
    def __init__(self):
        self.proxies = []

    def add_proxy(self, proxy):
        self.check_proxy(proxy)
        self.proxies.append(proxy)

    def check_pos(self, pos):
        if isinstance(pos, int):
            raise ValueError('Index must be int', type(pos))
        size = len(self.proxies)
        if pos < 0:
            raise ValueError('Index must be positive!', pos)
        if pos > size:
            raise ValueError('Index must smaller than size!', pos)

    @staticmethod
    def check_proxy(proxy):
        if not isinstance(proxy, Proxy):
            raise ValueError('Proxy type error!', type(proxy))

    '''
    pos 默认为0
    '''

    def get_proxy(self, pos=0):
        return self.proxies[pos]

    def set_proxy(self, pos, proxy):
        self.check_proxy(proxy)
        self.check_pos(pos)
        self.proxies[pos] = proxy

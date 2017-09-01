from src.proxymanager import *


def format_proxy(proxy):
    if not isinstance(proxy, Proxy):
        raise ValueError('Proxy type Error!')
    return {
        "http": "http://%s:%s" % (proxy.ip, proxy.port),
        "https": "http://%s:%s" % (proxy.ip, proxy.port)
    }

from src.proxymanager import *
import requests
import json

base_url = 'http://127.0.0.1:8000/'


def format_proxy(proxy):
    if not isinstance(proxy, Proxy):
        raise ValueError('Proxy type Error!')
    return {
        "http": "http://%s:%s" % (proxy.ip, proxy.port),
        "https": "http://%s:%s" % (proxy.ip, proxy.port)
    }


def acquire_proxies(size):
    params = {
        'count': size,
        'country': '国内'
    }
    result = requests.get(base_url, params=params)
    proxies = json.loads(result.text)
    proxy_list = [Proxy(proxies[i][0], proxies[i][1]) for i in range(len(proxies))]
    return proxy_list


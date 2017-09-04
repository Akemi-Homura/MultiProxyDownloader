import unittest
from src.adapter import *
from src.proxymanager import *


class TestAdapter(unittest.TestCase):
    def test_format_proxy(self):
        proxy = Proxy('127.0.0.1', 10805)
        d = {
            'http': 'http://127.0.0.1:10805',
            'https': 'http://127.0.0.1:10805'
        }
        self.assertEqual(format_proxy(proxy), d)
        self.assertRaises(ValueError, format_proxy, 2)
        self.assertRaises(ValueError, format_proxy, None)

    def test_acquire_proxies(self):
        proxies = acquire_proxies(10)
        self.assertTrue(isinstance(proxies[0], Proxy))
        self.assertEqual(len(proxies), 10)


if __name__ == '__main__':
    unittest.main()

from src.proxymanager import *
import unittest


class TestProxy(unittest.TestCase):
    def setUp(self):
        self.ip = '127.0.0.1'
        self.ip2 = '192.168.1.1'
        self.port = 40024
        self.port2 = 10805
        self.ip_msg = '%s doesn\'t equal to %s'
        self.port_msg = '%d doesn\'t equal to %d'
        self.bad_ips = ['256.0.1.1', '120.15.1', '1233.45.2.1']
        self.bad_ports = [-1, 0, 70000, 65536]

    def test_ip(self):
        proxy = Proxy()
        proxy.ip = self.ip
        self.assertEqual(proxy.ip, self.ip, self.ip_msg % (proxy.ip, self.ip))
        proxy.ip = self.ip2
        self.assertEqual(proxy.ip, self.ip2, self.ip_msg % (proxy.ip, self.ip2))

    def test_port(self):
        proxy = Proxy()
        proxy.port = self.port
        self.assertEqual(proxy.port, self.port, self.port_msg % (proxy.port, self.port))

        proxy.port = self.port2
        self.assertEqual(proxy.port, self.port2, self.port_msg % (proxy.port, self.port2))

    def test_constructor(self):
        proxy = Proxy(self.ip, self.port)
        self.assertEqual(proxy.ip, self.ip)
        self.assertEqual(proxy.port, self.port)

        proxy = Proxy(self.ip2, self.port2)
        self.assertEqual(proxy.ip, self.ip2)
        self.assertEqual(proxy.port, self.port2)

    def test_eq(self):
        proxy1 = Proxy(self.ip, self.port)
        proxy2 = Proxy(self.ip, self.port)
        self.assertEqual(proxy1, proxy2)

    def test_bad_ip(self):
        for bad_ip in self.bad_ips:
            self.assertRaises(ValueError, self.set_bad_ip, bad_ip)

    def test_bad_port(self):
        for bad_port in self.bad_ports:
            self.assertRaises(ValueError, self.set_bad_port, bad_port)

    def set_bad_ip(self, ip):
        proxy = Proxy()
        proxy.ip = ip

    def set_bad_port(self, port):
        proxy = Proxy()
        proxy.port = port


if __name__ == '__main__':
    unittest.main()

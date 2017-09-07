import unittest
from unittest.mock import *
import requests
from src.downloader import *


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.url = 'http://m2.26ts.com/20158CN-097.mp4'
        self.filename = 'test.mp4'
        self.file_size = 47887746

    def test_download(self):
        url, start, end, filename = 'url', 1, 100, 'name'
        proxy = {
            'http': 'http://127.0.0.1:80',
            'https': 'http://127.0.0.1:80'
        }
        headers = {'Range': 'bytes=%d-%d' % (start, end)}
        with patch.object(requests, 'get') as mock_get:
            with patch('builtins.open') as mocked_open:
                r, fp = Mock(), Mock()
                mock_get.return_value = r
                r.content = '123'
                mocked_open.return_value = fp
                download(url, start, end, filename, proxy)

        mock_get.assert_called_once_with(url, headers=headers, stream=True, proxies=proxy)
        fp.seek.assert_called_once_with(start)
        fp.tell.assert_called_once_with()
        fp.write.assert_called_once_with(r.content)
        fp.close.assert_called_once_with()

    def test_create_file(self):
        filename, file_size = self.filename, 123
        with patch('builtins.open') as mocked_open:
            fp = Mock()
            mocked_open.return_value = fp
            create_file(filename, file_size)
        mocked_open.assert_called_once_with(filename, 'wb')
        fp.truncate.assert_called_once_with(file_size)
        fp.close.assert_called_once_with()

    def test_get_file_size(self):
        self.assertEqual(get_file_size(self.url), self.file_size)

    @patch('builtins.list')
    def test_format_proxies(self, mocked_list):
        add_local_proxies(mocked_list)
        self.assertEqual(mocked_list.append.call_count,2)


if __name__ == '__main__':
    unittest.main()

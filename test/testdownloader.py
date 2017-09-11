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
    def test_add_local_proxies(self, mocked_list):
        add_local_proxies(mocked_list)
        self.assertEqual(mocked_list.append.call_count, 2)

    @patch('src.downloader.create_file')
    @patch('src.downloader.get_file_size')
    def test_assign_download(self,mocked_get_file_size,mocked_create_file):
        mocked_get_file_size.return_value = 1000
        thread_num = 7
        threads_pool = Mock()
        threads_pool.max_thread_num = thread_num
        assign_download(self.url, threads_pool)
        self.assertEqual(threads_pool.put.call_count, thread_num)
        mocked_create_file.assert_called_once_with('20158CN-097.mp4', 1000)

if __name__ == '__main__':
    unittest.main()

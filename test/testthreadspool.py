import unittest
from src.threadspool import *
from unittest.mock import *
import threading


class TestThreadsPool(unittest.TestCase):
    def setUp(self):
        self.thread_pool = ThreadsPool()

    def test_check_positive_num(self):
        self.assertTrue(ThreadsPool.check_positive_num(1))
        self.assertRaises(ValueError, ThreadsPool.check_positive_num, -1)
        self.assertRaises(ValueError, ThreadsPool.check_positive_num, 0)

    def test_put(self):
        w = (print, '1', None)
        w1 = (1, '1', None)
        thread_pool = ThreadsPool()
        with patch.object(ThreadsPool, 'generate_thread') as generate_thread:
            with patch.object(thread_pool.q, 'put') as mock_put:
                thread_pool.put(w[0], w[1])

        self.assertRaises(TypeError, thread_pool.put, w1[0], w1[1])
        self.assertRaises(TypeError, thread_pool.put, w[0], w[1], 1)
        generate_thread.assert_called_once_with()
        mock_put.assert_called_once_with(w)

    def test_generate_thread(self):
        with patch('threading.Thread') as mock:
            t = mock.return_value
            self.thread_pool.generate_thread()
            t.start.assert_called_once_with()

    def test_call(self):
        current_thread = threading.current_thread()
        thread_pool = self.thread_pool

        with patch.object(thread_pool, 'generate_list') as glist:
            with patch.object(thread_pool.q, 'get') as mock_get:
                with patch.object(threading, 'current_thread') as cthread:
                    mock_get.return_value = StopEvent
                    cthread.return_value = current_thread
                    thread_pool.call()
        '''
        :type glist:MagicMock
        :type cthread:MagicMock    
        '''
        glist.append.assert_called_once_with(current_thread)
        glist.remove.assert_called_once_with(current_thread)

if __name__ == '__main__':
    unittest.main()

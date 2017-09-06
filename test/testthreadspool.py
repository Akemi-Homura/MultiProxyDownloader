import unittest
from src.threadspool import *
from unittest.mock import *
import threading
import time


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
        func = Mock(return_value=1)
        args = '1'
        callback = Mock()
        w = (func, args, callback)
        with patch.object(thread_pool, 'generate_list') as glist:
            with patch.object(thread_pool, 'worker_state') as mock_ws:
                with patch.object(thread_pool, 'free_list') as mock_fl:
                    with patch.object(threading, 'current_thread', ) as mock_ct:
                        mock_ct.return_value = current_thread
                        thread_pool.q.put(w)
                        thread_pool.call()
        '''
        :type glist:MagicMock
        :type cthread:MagicMock    
        '''
        glist.append.assert_called_once_with(current_thread)
        glist.remove.assert_called_once_with(current_thread)
        mock_ws.assert_called_once_with(mock_fl, current_thread)
        func.assert_called_once_with(*args)
        callback.assert_called_once_with(True, 1)

    def test_close(self):
        thread_pool = self.thread_pool
        with patch.object(thread_pool, '_ThreadsPool__put_stop_event') as pse:
            thread_pool.close()
        pse.assert_called_once_with()

    def test_terminate(self):
        thread_pool = self.thread_pool
        with patch.object(thread_pool, '_ThreadsPool__put_stop_event') as pse:
            thread_pool.terminate()
        pse.assert_called_once_with()

    def test_worker_state(self):
        thread_pool = self.thread_pool
        mock_list = Mock()
        thread = threading.current_thread()
        with thread_pool.worker_state(mock_list, thread):
            pass
        mock_list.append.assert_called_once_with(thread)
        mock_list.remove.assert_called_once_with(thread)

    def test_await(self):
        thread_pool = self.thread_pool
        end = Mock()

        def add(a, b):
            a + b

        for i in range(100):
            thread_pool.put(add, (i, i + 1))
        thread_pool.await()
        thread_pool.close()
        end()
        end.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()

import threading
from queue import Queue
import contextlib

# 线程结束事件
StopEvent = object()


class ThreadsPool(object):
    def __init__(self, max_thread_num=5, max_task_num=None):
        ThreadsPool.check_positive_num(max_thread_num)
        self.max_thread_num = max_thread_num
        if max_task_num:
            self.q = Queue(max_task_num)
        else:
            self.q = Queue()
        self.generate_list = []
        self.free_list = []
        self.cancel = False
        self.terminate = False

    @staticmethod
    def check_positive_num(num):
        if not isinstance(num, int):
            raise ValueError('Num type Error!Actual {}, excepted {}', type(num), type(int))
        if num < 1:
            raise ValueError('Num must be positive!Actual value is %d' % num)
        return True

    def put(self, func, args, callback=None):
        if self.cancel:
            return
        if not callable(func):
            raise TypeError('Func must be callable!')
        if callback and not callable(callback):
            raise TypeError('Callback must be callable!')
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_thread_num:
            self.generate_thread()
        # 函数三元组,函数名,参数,回调函数
        w = (func, args, callback)
        self.q.put(w)

    def generate_thread(self):
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        current_thread = threading.current_thread()
        self.generate_list.append(current_thread)
        event = self.q.get()
        while event != StopEvent:
            func, args, callback = event
            try:
                result = func(args)
                success = True
            except Exception as e:
                print('Exception', e)
                result = None
                success = False
            if callback is not None:
                try:
                    callback(success, result)
                except Exception as e:
                    pass
            with self.worker_state(self.free_list, current_thread):
                if self.terminate:
                    event = StopEvent
                else:
                    event = self.q.get()
        else:
            self.generate_list.remove(current_thread)

    def close(self):
        self.cancel = True
        self.__put_stop_event()

    def terminate(self):
        self.terminate = True
        self.__put_stop_event()

    def await(self):
        while len(self.free_list) < len(self.generate_list):
            pass

    def __put_stop_event(self):
        active_thread_num = len(self.generate_list)
        while active_thread_num:
            self.q.put(StopEvent)
            active_thread_num -= 1

    @contextlib.contextmanager
    def worker_state(self, state_list, thread):
        state_list.append(thread)
        try:
            yield
        finally:
            state_list.remove(thread)

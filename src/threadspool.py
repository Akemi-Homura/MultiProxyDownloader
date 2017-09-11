import threading
from queue import Queue
import contextlib

StopEvent = object()
timeout = 3


class ThreadsPool(object):
    def __init__(self, max_thread_num=5, max_task_num=None):
        if max_task_num:
            self.q = Queue(max_task_num)
        else:
            self.q = Queue()
        self.max_thread_num = 5
        self.generate_list = []
        self.free_list = []
        self.cancel = False
        self.terminal = False

    @staticmethod
    def check_positive_num(num):
        if not isinstance(num, int):
            raise TypeError('Excepted type is {}\nActual type is {}'.format(type(int), type(num)))
        if num < 1:
            raise ValueError('Num must be positive!Actual is %d' % num)
        return True

    def put(self, func, args, callback=None):
        if not callable(func):
            raise TypeError('Func must be callable!')
        if callback is not None and not callable(callback):
            raise TypeError('Callback must be callable or none!')
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_thread_num:
            self.generate_thread()

        w = (func, args, callback)
        self.q.put(w)

    def generate_thread(self):
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        current_thread = threading.current_thread()
        self.generate_list.append(current_thread)
        event = self.q.get()
        if self.cancel:
            return
        while event != StopEvent:
            func, args, callback = event
            try:
                result = func(*args)
                success = True
            except Exception as e:
                e.with_traceback()
                result = None
                success = False
            try:
                callback(success, result)
            except Exception as e:
                # e.with_traceback()
                pass

            with self.worker_state(self.free_list, current_thread):
                if self.terminal:
                    event = StopEvent
                else:
                    try:
                        event = self.q.get(timeout=timeout)
                    except Exception:
                        event = StopEvent

        else:
            self.generate_list.remove(current_thread)

    def close(self):
        self.cancel = True
        self.__put_stop_event()

    def terminate(self):
        self.terminal = True
        self.__put_stop_event()

    def await(self):
        while not self.q.empty():
            pass

    def __put_stop_event(self):
        active_thread_num = len(self.generate_list)
        while active_thread_num > 0:
            self.q.put(StopEvent)
            active_thread_num -= 1

    @contextlib.contextmanager
    def worker_state(self, state_list: list, thread):
        state_list.append(thread)
        try:
            yield
        finally:
            state_list.remove(thread)

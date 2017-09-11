import sys
from src.adapter import *
from src.threadspool import *

local_proxy = [Proxy('127.0.0.1', 80), Proxy('127.0.0.1', 1080)]


def download(url, start, end, filename, proxy):
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    r = requests.get(url, headers=headers, stream=True, proxies=proxy)

    fp = open(filename, 'r+b')
    fp.seek(start)
    fp.write(r.content)
    fp.close()


def get_file_size(url):
    r = requests.head(url)
    return int(r.headers['content-length'])


def create_file(filename, file_size):
    fp = open(filename, 'wb')
    fp.truncate(file_size)
    fp.close()


def assign_download(url: str, thread_pool: ThreadsPool, proxies=[], filename=None):
    if len(proxies) == 0:
        add_local_proxies(proxies)
    file_size = get_file_size(url)
    if filename is None:
        filename = url.split('/')[-1]
    create_file(filename, file_size)
    thread_num = thread_pool.max_thread_num
    '''
    :param part: 每一片文件的大小
    '''

    def callback(success: bool, result: int):
        if success is True:
            print('Downloading part %d success!' % result)
        else:
            print('Downloading part %d fail!' % result)

    part = file_size // thread_num
    for i in range(thread_num):
        start = part * i
        if i == thread_num - 1:
            end = file_size
        else:
            end = start + part
        index = i % len(proxies)
        thread_pool.put(download, (url, start, end, filename, proxies[index]), callback)

    thread_pool.await()
    thread_pool.close()


def add_local_proxies(proxies):
    for proxy in local_proxy:
        proxies.append(format_proxy(proxy))


def prepare_download(url, proxy_num=10, thread_num=6):
    proxies = acquire_proxies(proxy_num)
    formatted_proxies = list(map(format_proxy, proxies))
    threads_pool = ThreadsPool(thread_num)
    assign_download(url, threads_pool, formatted_proxies)


if __name__ == '__main__':
    # _url = sys.argv[1]
    prepare_download('http://m2.26ts.com/20158CN-097.mp4', 0, 5)

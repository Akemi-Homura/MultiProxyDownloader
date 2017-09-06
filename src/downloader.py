import sys
from src.adapter import *
from src.threadspool import *

local_proxy = [Proxy('127.0.0.1', 80), Proxy('127.0.0.1', 1080)]


def download(start, end, filename, proxy):
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    r = requests.get(url, headers=headers, stream=True, proxies=proxy)

    with open(filename, 'r+b') as fp:
        fp.seek(start)
        var = fp.tell()
        fp.write(r.content)


def create_file(filename):
    r = requests.head(url)

    try:
        if filename is None:
            filename = url.split('/')[-1]
        file_size = int(r.headers['content-length'])
    except:
        print('URL error or don\'t support multi thread.')
        return

    fp = open(filename, 'wb')
    fp.truncate(file_size)
    fp.close()
    return file_size


def assign_download(url, thread_num=5, proxies=[], filename=None):
    format_proxies(proxies)
    file_size=create_file(filename)
    '''
    :param part: 每一片文件的大小
    '''

    def callback(success: bool, result: int):
        if success is True:
            print('Downloading part %d success!' % result)
        else:
            print('Downloading part %d fail!' % result)

    thread_pool = ThreadsPool(thread_num)
    part = file_size // thread_num
    for i in range(thread_num):
        start = part * i
        if i == thread_num - 1:
            end = file_size
        else:
            end = start + part
        index = i % len(proxies)
        thread_pool.put(download, (start, end, filename, proxies[index]), callback)

    thread_pool.await()
    thread_pool.close()


def format_proxies(proxies):
    for proxy in local_proxy:
        if proxy not in proxies:
            proxies.append(proxy)
    map(format_proxy, proxies)


if __name__ == '__main__':
    url = sys.argv[1]

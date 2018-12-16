import requests
import asyncio
import threading
import queue
import time
from multiprocessing import Process, cpu_count
q = queue.Queue()

def count_queue():
    flag = 0
    while True:
        num = q.qsize() - flag
        flag = q.qsize()
        print('***********qps: {0}************'.format(num))
        time.sleep(1)



async def async_request(i, url, loop):
    while True:
        for j in range(1):
            # print('******task:{0}*****interface: {1}'.format(str(i), str(j)))
            start = time.time()
            res = await loop.run_in_executor(None, requests.get, url)
            # await asyncio.sleep(random.randint(0, 1))
            # print('**********end**task:{0}******interface: {1}**'.format(str(i), str(j)))
            q.put(True)

class AsyncPool(object):

    def __init__(self, num, loop):
        self.num = num
        self.task = None
        self.args = ()
        self.kwargs = {}
        self.loop = loop

    def add_task(self, task, *args, **kwargs):
        self.task = task
        self.args = args
        self.kwargs = kwargs
        return self

    def async_works(self):
        tasks = []
        for t in range(self.num):
            tasks.append(self.task(t, *self.args, **self.kwargs))
        self.loop.run_until_complete(asyncio.gather(*tasks))


threading.Thread(target=count_queue).start()
loop = asyncio.get_event_loop()
async_pool = AsyncPool(1000, loop)
async_pool.add_task(async_request, 'http://127.0.0.1:8080/ping', loop)
# async_pool.async_works()

for i in range(1):
    Process(target=async_pool.async_works).start()

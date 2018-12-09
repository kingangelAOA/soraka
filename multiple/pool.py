from concurrent import futures
from inspect import isfunction
from .exceptions import TaskTypeError
from .qps import Qps
import aiohttp

class Pool(object):
    def __init__(self, num, qps_num):
        self.num = num
        self.task = None
        self.qps = Qps(qps_num)

    def add_task(self, fun):
        if not isfunction(fun):
            raise TaskTypeError('task is not a function')
        self.task = fun

    def run_task(self):
        while True:
            self.qps.get_sign()
            self.task()

    def run(self):
        with futures.ThreadPoolExecutor(max_workers=self.num) as executor:
            executor.submit(self.run_task)


async def task():
    r = await aiohttp.get('http://www.baidu.com')
    print(r)

p = Pool(4, 100)

p.add_task(task)
p.run()
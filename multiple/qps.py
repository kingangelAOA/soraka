from queue import Queue
from time import sleep
import threading

class Qps(object):
    def __init__(self, num):
        self.num = num
        self.q = Queue(1)
        self.t = threading.Thread(target=self.init_sign)
        self.sign_start()

    def init_sign(self):
        while True:
            self.q.put(True)
            sleep(1/self.num)

    def get_sign(self):
        return self.q.get()

    def sign_start(self):
        self.t.start()
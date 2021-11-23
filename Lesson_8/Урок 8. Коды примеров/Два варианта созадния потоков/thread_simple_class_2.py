"""Отдельный класс-поток"""

import time
from threading import Thread


class ClockThread(Thread):
    """Класс-наследник потока"""
    def __init__(self, interval):
        super().__init__()
        self.daemon = True
        self.interval = interval

    def run(self):
        while True:
            print(f"Текущее время: {time.ctime()}")
            time.sleep(self.interval)


THR = ClockThread(1)
THR.start()
THR.join()

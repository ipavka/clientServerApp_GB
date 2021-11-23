"""Главный поток и дочерний поток (демон)"""

import threading
import time
from logging import info, basicConfig, INFO


def demo_thr_func(name):
    """Логика функции для дочернего потока"""
    info(f"Дочерний поток {name} стартует")
    time.sleep(2)
    info(f"Дочерний поток {name} завершается")


if __name__ == "__main__":
    basicConfig(
        format="%(asctime)s: %(message)s",
        level=INFO,
        datefmt="%H:%M:%S")
    info("Приложение: до создания дочернего потока")
    THR_OBJ = threading.Thread(target=demo_thr_func, args=(1,), daemon=True)
    info("Приложение: до старта дочернего потока")
    THR_OBJ.start()
    info("Приложение: не ждет, пока завершится дочерний поток")


"""
Приложение не ждет завершения дочернего потока.
"""

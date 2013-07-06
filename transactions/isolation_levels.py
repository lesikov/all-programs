#!/usr/bin/python3

import os
import sys
import time
import sqlite3
import threading


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-10s) %(message)s')

def foo():
    print('foo:before')
    ready.wait()
    print('foo:after')

def bar():
    print('bar:before')
    print('bar:after')

if __name__ == '__main__':
    # События - простой объект синхронизации: события представляют
    # внутренний флаг и потоки могут ждать, пока флаг будет установлен.
    ready = threading.Event()

    threads = [
        threading.Thread(name='Foo', target=foo),
        threading.Thread(name='Bar', target=bar)
    ]

    [t.start() for t in threads]

    time.sleep(1)
    ready.set()
    [t.join() for t in threads]

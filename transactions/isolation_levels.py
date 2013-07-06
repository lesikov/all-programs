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
    print('foo')

def bar():
    print('bar')


if __name__ == '__main__':
    threads = [
        threading.Thread(name='Foo', target=foo),
        threading.Thread(name='Bar', target=bar)
    ]

    [t.start() for t in threads]

    [t.join() for t in threads]

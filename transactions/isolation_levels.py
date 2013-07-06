#!/usr/bin/python3

import os
import sys
import time
import sqlite3
import threading


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-10s) %(message)s')

def writer():
    logging.debug('connecting')
    with sqlite3.connect('bank.db') as conn:
        c = conn.cursor()
        logging.debug('connected')
        c.execute('UPDATE donation SET blood_type="O+"')
        logging.debug('changes made')
        logging.debug('waiting to synchronize')
        ready.wait() # синхронизация
        logging.debug('PAUSING')
        time.sleep(1)
        conn.commit()
        logging.debug('CHANGES COMMITTED')
    return

def reader():
    with sqlite3.connect('bank.db') as conn:
        c = conn.cursor()
        logging.debug('waiting to synchronize')
        ready.wait() # синхронизация
        logging.debug('wait over')
        c.execute('SELECT * from donation')
        logging.debug('SELECT EXECUTED')
        results = c.fetchall()
        logging.debug(results)
        logging.debug('results fetched')
    return


if __name__ == '__main__':
    # События - простой объект синхронизации: события представляют
    # внутренний флаг и потоки могут ждать, пока флаг будет установлен.
    ready = threading.Event()

    threads = [
        threading.Thread(name='Reader', target=reader),
        threading.Thread(name='Writer', target=writer),
    ]

    [t.start() for t in threads]

    time.sleep(1)
    logging.debug('setting ready')
    ready.set()
    [t.join() for t in threads]

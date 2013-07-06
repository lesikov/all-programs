# coding: utf-8
#!/usr/bin/python3

import os
import sys
import time
import sqlite3
import threading

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-10s) %(message)s')


#  Вывод строки до изменений
with sqlite3.connect('bank.db') as conn:
    c = conn.cursor()
    c.execute('SELECT * FROM donation')
    result = c.fetchone()
    c.close()

    print('BEFORE CHANGES:')
    print(result, end='\n\n')


def writer():
    logging.debug('connecting')
    with sqlite3.connect('bank.db') as conn:
        c = conn.cursor()
        logging.debug('connected')

        # Изменения значения даты на текущую локальную
        c.execute('UPDATE donation SET donate_on=DATETIME("now", "localtime")')
        logging.debug('changes made: UPDATE donation SET donate_on=...')

        logging.debug('waiting to synchronize')
        ready.wait() # синхронизация
        logging.debug('PAUSING')
        time.sleep(1)

        # Применение изменений в базу данных
        conn.commit()
        logging.debug('CHANGES COMMITTED')
    return

def reader():
    with sqlite3.connect('bank.db') as conn:
        c = conn.cursor()

        logging.debug('waiting to synchronize')
        ready.wait() # синхронизация
        logging.debug('wait over')

        # Выборка строк в потоке (в это время в потоке Writer была начата транзакция и выполнено изменение)
        c.execute('SELECT * from donation')
        logging.debug('SELECT EXECUTED')
        result = c.fetchone()
        # В потоке Writer транзакция на это время не применена
        logging.debug('result fetched')
        logging.debug(result)
    return


if __name__ == '__main__':
    # События - простой объект синхронизации: события представляют
    # внутренний флаг и потоки могут ждать, пока флаг будет установлен.
    ready = threading.Event()

    threads = [
        threading.Thread(name='Writer', target=writer),
        threading.Thread(name='Reader', target=reader),
    ]

    [t.start() for t in threads]

    time.sleep(1)
    logging.debug('setting ready')
    ready.set()
    [t.join() for t in threads]

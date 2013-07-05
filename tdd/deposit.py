#!/usr/bin/env python3

import math
import time
import datetime
import json
import sqlite3
import requests


OPENEXCHANGERATES_APP_ID = 'd57f0fccee6548ed8fae64ddf9197ec1'


class DepositInformer:
    """
    Для получения актуального курса валют информатор использует сервис
    https://openexchangerates.org, который предоставляет данные в формате JSON.
    """
    _URL_OEC = 'http://openexchangerates.org/api/latest.json?app_id={}'

    def __init__(self, init_deposit=None, debug=False):
        self.url = self._URL_OEC.format(OPENEXCHANGERATES_APP_ID)

        if (init_deposit):
            self.deposit = init_deposit
            self._commit_changes()
        else:
            self._deposit, self.timestamp = self.get_latest_value()

        self.debug = debug


    @property
    def deposit(self):
        return self._deposit

    @deposit.setter
    def deposit(self, value):
        self._deposit = value
        self.timestamp = int(time.time())

    def update(self):
        """Увеливает депозит с учётом процента и применить изменения."""
        self.grow_deposit()
        self._commit_changes()

    def get_latest_value(self):
        """Возвращает последнее добавленное значение депозита."""
        conn = sqlite3.connect('data/deposit.db')
        c = conn.cursor()
        c.execute('SELECT * FROM deposits ORDER BY rowid DESC LIMIT 1')
        latest = c.fetchone()
        conn.close()
        return latest

    def get_rate(self, currency):
        """
        Получение отношения курса валюты к базовой (USD)

        Курс валюты задаётся тремя символами.
        Список доступных валют с полными именами можно посмотреть здесь:
        http://openexchangerates.org/api/currencies.json

        Обновление курса на сервере происходит один раз в час.
        """
        resp = requests.get(self.url)
        data = resp.json()
        try:
            return data['rates'][currency]
        except KeyError:
            raise KeyError('Invalid currency specified: {}'.format(currency))


    def grow_deposit(self):
        now = int(time.time())
        delta = self._delta_time()
        one_year = datetime.timedelta(days=365).total_seconds()

        rate = self.get_rate('EUR')
        self.deposit = self.deposit * math.pow(math.exp(1),
                                               rate / 10 * delta / one_year)

        if self.debug:
            print('Current deposit value: {}'.format(self.deposit))

        return self.deposit


    def _delta_time(self):
        now = int(time.time())
        return now - self.timestamp


    def _commit_changes(self):
        """Сохранение последних изменений."""
        conn = sqlite3.connect('data/deposit.db')
        c = conn.cursor()
        to_commit = (self.deposit, self.timestamp)
        c.execute('INSERT INTO deposits VALUES {}'.format(to_commit))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    informer = DepositInformer(debug=True)
    informer.update()

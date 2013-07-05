#!/usr/bin/env python3

import time
import datetime
import unittest
from mock import patch, Mock

from deposit import DepositInformer


class DepositInformerTests(unittest.TestCase):
    @patch('requests.get')
    def test_invalid_rate(self, get_mock):
        data = {
          'rates': {
            'AED': 3.672626
          }
        }
        get_mock.return_value.json.return_value = data
        informer = DepositInformer()
        self.assertRaises(KeyError, informer.get_rate, 'INV')


    @patch.object(DepositInformer, 'get_rate')
    @patch.object(DepositInformer, '_delta_time')
    def test_grow_deposit_1day(self, rate_mock, delta_mock):
        deposit = 100
        informer = DepositInformer(deposit)
        rate_mock.return_value = 0.778564
        delta_mock.return_value = datetime.timedelta(days=1).total_seconds()

        new_deposit = informer.grow_deposit()
        self.assertAlmostEqual(new_deposit, 100.02133279)

    @patch.object(DepositInformer, 'get_rate')
    @patch.object(DepositInformer, '_delta_time')
    def test_grow_deposit_2days(self, rate_mock, delta_mock):
        deposit = 100
        informer = DepositInformer(deposit)
        rate_mock.return_value = 0.778564
        delta_mock.return_value = datetime.timedelta(days=2).total_seconds()

        new_deposit = informer.grow_deposit()
        self.assertAlmostEqual(new_deposit, 100.04267014)


if __name__ == '__main__':
    unittest.main()

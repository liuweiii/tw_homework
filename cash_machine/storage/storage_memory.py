# -*- coding: utf-8 -*-
from cash_machine.test_data import products


class StorageMemory(object):
    def __init__(self):
        self.products = products
        self.tables = {
            "product": self.products
        }

    def get(self, name, key):
        try:
            return self.tables[name][key]
        except KeyError:
            return []

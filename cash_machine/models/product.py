# -*- coding: utf-8 -*-
from cash_machine.storage.storage import storage
from cash_machine.common.exception import ProductNotFoundException, ProductParseException
from cash_machine.models.discount import NoDiscount, Discount95, Buy2Save1


class Product(object):
    def __init__(self, name, unit, price, clazz, code, discounts):
        self.name = name
        self.unit = unit
        self.price = price
        self.clazz = clazz
        self.code = code
        self._discounts = set()
        self._discounts_names = set()
        self.__set_discounts(discounts)

    def __set_discounts(self, discounts):
        self._discounts = set(discounts)
        self._discounts_names = set(str(x) for x in self._discounts)

    def set_discounts(self, discounts):
        self.__set_discounts(discounts)
        storage.set("product", self.code, "discounts", list(self._discounts))

    def discount(self, count):
        if self.has_discount(Buy2Save1()):
            return Buy2Save1().out(self, count)
        if self.has_discount(Discount95()):
            return Discount95().out(self, count)
        return NoDiscount().out(self, count)

    def has_discount(self, discount):
        if isinstance(discount, str):
            return discount in self._discounts_names
        return discount in self._discounts

    @staticmethod
    def __fill_fields(**data):
        return Product(**data)

    @staticmethod
    def get_by_code(code):
        result = storage.get("product", code=code)
        if len(result) == 0:
            raise ProductNotFoundException()
        try:
            return Product.__fill_fields(**result)
        except TypeError:
            raise ProductParseException()

    @staticmethod
    def get_products():
        result = storage.get_all("product")
        products = []
        for key in result:
            products.append(Product.__fill_fields(**result[key]))
        return products

    @staticmethod
    def reset_products():
        products = Product.get_products()
        for product in products:
            product.set_discounts([NoDiscount])

import unittest
from cash_machine.models.discount import Discount95, Buy2Save1, NoDiscount, Discount
from cash_machine.models.product import Product


class TestNoDiscount(unittest.TestCase):
    def __test_discount(self, discount, wanted_total_price, wanted_save_price):
        product = Product(name="apple", unit="", price=5.5, clazz="", code="", discounts=[discount])
        total_price, save_price, _ = discount.out(product, 3)
        self.assertEqual(int(total_price * 1000) / 10, wanted_total_price)
        self.assertEqual(int(save_price * 1000) / 10, wanted_save_price)

    def test_no_discount_out(self):
        self.__test_discount(NoDiscount(), 1650, 0)

    def test_discount95_out(self):
        self.__test_discount(Discount95(), 1567, 82)

    def test_buy2save1_out(self):
        self.__test_discount(Buy2Save1(), 1100, 550)

    def test_summarize_nothing(self):
        Discount.clean_summarize()
        product = Product(name="apple", unit="", price=5.5, clazz="", code="", discounts=[Buy2Save1])
        Buy2Save1().out(product, 2)
        self.assertEqual(None, Discount.summarize())

    def test_summarize_with_message(self):
        Discount.clean_summarize()
        product = Product(name="apple", unit="", price=5.5, clazz="", code="", discounts=[Buy2Save1])
        Buy2Save1().out(product, 3)
        self.assertEqual(2, len(Discount.summarize()))

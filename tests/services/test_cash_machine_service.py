# -*- coding: utf-8 -*-
import unittest
import mock
from cash_machine.services.cash_machine_service import generate_bill, set_discount
from cash_machine.models.product import Product
from cash_machine.models.discount import NoDiscount, Discount95, Buy2Save1
from werkzeug.datastructures import ImmutableDict


class TestCashMachineService(unittest.TestCase):
    @mock.patch("cash_machine.models.product.Product.get_by_code")
    def test__generate_bill_ok(self, mock_get):
        mock_get.return_value = Product(name="apple", unit="", price=5.5, clazz="", code="ITEM000001",
                                        discounts=[NoDiscount])
        shop_list_string = u"""[
                                "ITEM000001",
                                "ITEM000001"
                            ]"""
        result, bill = generate_bill(shop_list_string)
        self.assertTrue(result)
        self.assertEqual(bill.total_price, 11)

    def test__generate_bill_value_error(self):
        shop_list_string = u"""[
                                xx "ITEM000001"
                            ]"""
        result, message = generate_bill(shop_list_string)
        self.assertFalse(result)
        self.assertEqual(message, u"输入参数有误")

    @mock.patch("cash_machine.models.product.Product.get_by_code")
    def test__set_discount(self, mock_get):
        mock_get.return_value = Product(name="apple", unit="", price=5.5, clazz="", code="ITEM000001",
                                        discounts=[Discount95()])
        product = Product.get_by_code("ITEM000001")
        self.assertTrue(product.has_discount(Discount95()))
        self.assertEqual(product.discount_length(), 1)
        discount_list_string = ImmutableDict({'ITEM0000001.Buy2Save1': u'on'})
        set_discount(discount_list_string)
        self.assertTrue(product.has_discount(Buy2Save1()))
        self.assertEqual(product.discount_length(), 1)


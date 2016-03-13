import unittest
import mock
from cash_machine.models.product import Product
from cash_machine.common.exception import ProductNotFoundException, ProductParseException
from cash_machine.models.discount import NoDiscount


class TestProduct(unittest.TestCase):

    @mock.patch("cash_machine.storage.storage.storage.get")
    def test__get_by_code_succeed(self, mock_storage_get):
        mock_storage_get.return_value = {
            "name": "test_name",
            "unit": "test_unit",
            "price": 123,
            "clazz": "test_clazz",
            "discounts": "test_discount",
            "code": "ITEM000099"
        }
        p = Product.get_by_code("ITEM000099")
        self.assertEqual(p.code, "ITEM000099")
        self.assertEqual(p.name, "test_name")
        self.assertEqual(p.unit, "test_unit")
        self.assertEqual(p.price, 123)
        self.assertEqual(p.clazz, "test_clazz")

    @mock.patch("cash_machine.storage.storage.storage.get")
    def test__get_by_code_not_found(self, mock_storage_get):
        try:
            mock_storage_get.return_value = []
            Product.get_by_code("ITEM000000")
        except ProductNotFoundException:
            return
        self.assertEqual(0, 1, "The product is not found, but the result is succeed.")

    @mock.patch("cash_machine.storage.storage.storage.get")
    def test__get_by_code_parse_failed(self, mock_storage_get):
        try:
            mock_storage_get.return_value = {
                "name": "test_name_",
                "unit_": ""
            }
            Product.get_by_code("ITEM000000")
        except ProductParseException:
            return
        self.assertEqual(0, 1, "The key is error, but the result is succeed.")

    @mock.patch("cash_machine.storage.storage.storage.get_all")
    def test_get_products(self, mock_storage_get_all):
        mock_storage_get_all.return_value = {
            "ITEM01": {'code': "ITEM01", 'clazz': '', 'discounts': [], 'name': 't1', 'price': 12, 'unit': 'u'},
            "ITEM02": {'code': "ITEM02", 'clazz': '', 'discounts': [], 'name': 't2', 'price': 12, 'unit': 'u'}
        }
        products = Product.get_products()
        self.assertEqual(len(products), 2)
        for product in products:
            self.assertEqual(product.price, 12)

    def test_reset_products(self):
        Product.reset_products()
        products = Product.get_products()
        for product in products:
            self.assertTrue(product.has_discount(NoDiscount))
            self.assertEqual(product.discount_length(), 1)

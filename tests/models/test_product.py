import unittest
import mock
from cash_machine.models.product import Product
from cash_machine.common.exception import ProductNotFoundException, ProductParseException


class TestProduct(unittest.TestCase):

    @mock.patch("cash_machine.storage.storage.storage.get")
    def test__get_by_code_succeed(self, mock_storage_get):
        mock_storage_get.return_value = {
            "name": "test_name",
            "unit": "test_unit",
            "price": 123,
            "clazz": "test_clazz",
            "discount": "test_discount"
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

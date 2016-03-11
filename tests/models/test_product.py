import unittest
from cash_machine.models.product import Product
from cash_machine.common.exception import ProductNotFoundException


class TestProduct(unittest.TestCase):
    def test__get_by_code_succeed(self):
        p = Product.get_by_code("ITEM000002")
        self.assertEqual(p.code, "ITEM000002")

    def test__get_by_code_not_found(self):
        try:
            Product.get_by_code("ITEX000002")
        except ProductNotFoundException:
            return
        self.assertEqual(0, 1, "The product is not found, but the result is succeed.")

import unittest

from cash_machine.storage.storage import storage


class TestStorage(unittest.TestCase):
    def test__get_succeed(self):
        result = storage.get("product", "ITEM000002")
        self.assertGreaterEqual(len(result), 1)

    def test__get_failed(self):
        result = storage.get("product", "ITEX000002")
        self.assertEqual(len(result), 0)

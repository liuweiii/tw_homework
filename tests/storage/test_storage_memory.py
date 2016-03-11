import unittest

from cash_machine.storage.storage_memory import StorageMemory


class TestStorageMemory(unittest.TestCase):
    def test__get_succeed(self):
        storage = StorageMemory()
        result = storage.get("product", "ITEM000002")
        self.assertGreaterEqual(len(result), 1)

    def test__get_failed(self):
        storage = StorageMemory()
        result = storage.get("product", "ITEX000002")
        self.assertEqual(len(result), 0)

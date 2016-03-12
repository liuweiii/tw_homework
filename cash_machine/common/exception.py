class ProductParseException(Exception):
    def __init__(self, key):
        self._key = key

    @property
    def key(self):
        return self._key

    def __str__(self):
        return "Product parse failed for key[{0}] is not provided.".format(self.key)


class ProductNotFoundException(Exception):
    """Products from storage not found"""

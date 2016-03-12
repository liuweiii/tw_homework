from cash_machine.storage.storage import storage

from cash_machine.common.exception import ProductNotFoundException, ProductParseException


class Product(object):
    def __init__(self, name, unit, price, clazz, code, discount):
        self.name = name
        self.unit = unit
        self.price = price
        self.clazz = clazz
        self.code = code
        self._discount = discount

    def discount(self, count):
        return self._discount.out(self, count)

    @staticmethod
    def get_by_code(code):
        result = storage.get("product", code=code)
        if len(result) == 0:
            raise ProductNotFoundException()
        try:
            return Product(result["name"], result["unit"], float(result["price"]),
                           result["clazz"], code, result["discount"])
        except KeyError as e:
            raise ProductParseException(e.message)

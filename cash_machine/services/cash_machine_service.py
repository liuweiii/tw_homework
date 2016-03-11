# -*- coding: utf-8 -*-
from cash_machine.models.product import Product


def to_bill_list(shop_list):
    def decode(l):
        pairs = l.split("-")
        code_ = pairs[0]
        # no character '-' means count=1
        count_ = 1 if len(pairs) == 1 else int(pairs[1])
        return code_, count_

    products = dict()
    for item in shop_list:
        code, count = decode(item)
        product = Product.get_by_code(code)
        if code in products:
            count += products[code][1]
        products[code] = (product, count)
    return products


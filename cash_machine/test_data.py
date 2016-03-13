# -*- coding: utf-8 -*-
from models.discount import Buy2Save1, Discount95, NoDiscount

DEFAULT_CLAZZ = u"商品"

products = {
    "ITEM000001": {"name": u"羽毛球", "unit": u"个", "price": 1.00, "clazz": DEFAULT_CLAZZ, "discounts": [Buy2Save1(), NoDiscount(), Buy2Save1(), Buy2Save1()],
                   "code": "ITEM000001"},
    "ITEM000002": {"name": u"大米", "unit": u"斤", "price": 2.30, "clazz": DEFAULT_CLAZZ, "discounts": [NoDiscount()],
                   "code": "ITEM000002"},
    "ITEM000003": {"name": u"苹果", "unit": u"斤", "price": 5.50, "clazz": DEFAULT_CLAZZ, "discounts": [NoDiscount(),Discount95(),Buy2Save1()],
                   "code": "ITEM000003"},
    "ITEM000004": {"name": u"蛋糕", "unit": u"块", "price": 6.00, "clazz": DEFAULT_CLAZZ, "discounts": [Discount95()],
                   "code": "ITEM000004"},
    "ITEM000005": {"name": u"可口可乐", "unit": u"瓶", "price": 3.00, "clazz": DEFAULT_CLAZZ, "discounts": [Buy2Save1()],
                   "code": "ITEM000005"},
}

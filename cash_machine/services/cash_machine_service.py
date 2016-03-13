# -*- coding: utf-8 -*-
import json
from cash_machine.common.exception import ProductNotFoundException
from cash_machine.models.product import Product
from cash_machine.models.bill import Bill


def _to_bill_list(shop_list):
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


def _render_out(bill_list):
    products_describe = []
    total_price = 0
    save_total_price = 0
    for key in bill_list.keys():
        product = bill_list[key][0]
        count = bill_list[key][1]
        this_product_total, this_product_save, this_product_total_describe = product.discount(count)
        total_price += this_product_total
        save_total_price += this_product_save
        products_describe.append(u"名称：%s，数量：%d %s，单价：%.2f（元），%s" %
                                 (product.name, count, product.unit, product.price, this_product_total_describe))
    return Bill(products_describe, total_price, save_total_price)


def generate_bill(shop_list_string):
    try:
        shop_list = json.loads(shop_list_string)
        bill_list = _to_bill_list(shop_list)
        return True, _render_out(bill_list)
    except ValueError:
        return False, u"输入参数有误"
    except ProductNotFoundException:
        return False, u"输入的条形码找不到对应商品"
    except Exception as e:
        return False, u"这个错误[{0}]没被考虑到... ...".format(e.message)


def get_products():
    return Product.get_products()

# -*- coding: utf-8 -*-
import copy


class Discount(object):
    def out(self, product, count):
        raise NotImplementedError()

    _sum_describe = []

    @staticmethod
    def summarize():
        if len(Discount._sum_describe) == 0:
            return None
        Discount._sum_describe[0:0] = [u"买二赠一商品："]
        result = copy.deepcopy(Discount._sum_describe)
        Discount._sum_describe = []
        return result

    @staticmethod
    def from_string(discount_string):
        if discount_string == "NoDiscount":
            return NoDiscount()
        if discount_string == "Buy2Save1":
            return Buy2Save1()
        if discount_string == "Discount95":
            return Discount95()


class NoDiscount(Discount):
    def out(self, product, count):
        total_price = count * product.price
        save_price = 0
        return total_price, save_price, u"小计：%.2f（元）" % total_price

    def __str__(self):
        return "NoDiscount"

    def __eq__(self, other):
        return isinstance(other, NoDiscount)

    def __hash__(self):
        return hash("NoDiscount")


class Buy2Save1(Discount):

    def out(self, product, count):
        assert count > 0
        save_count = count / 3
        total_price = (count - save_count) * product.price
        save_price = save_count * product.price
        if save_count > 0:
            Discount._sum_describe.append(u"名称：{0}，数量：{1}".format(product.name, save_count))
        return total_price, save_price, u"小计：%.2f（元）" % total_price

    def __str__(self):
        return "Buy2Save1"

    def __eq__(self, other):
        return isinstance(other, Buy2Save1)

    def __hash__(self):
        return hash("Buy2Save1")


class Discount95(Discount):
    def out(self, product, count):
        original_price = product.price * count
        total_price = original_price * 0.95
        save_price = original_price - total_price
        return total_price, save_price, u"小计：%.2f（元），节省%.2f（元）" % (total_price, save_price)

    def __str__(self):
        return "Discount95"

    def __eq__(self, other):
        return isinstance(other, Discount95)

    def __hash__(self):
        return hash("Discount95")

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


class NoDiscount(Discount):
    def out(self, product, count):
        total_price = count * product.price
        save_price = 0
        return total_price, save_price, u"小计：%.2f（元）" % total_price


class Buy2Save1(Discount):

    def out(self, product, count):
        assert count > 0
        save_count = count / 3
        total_price = (count - save_count) * product.price
        save_price = save_count * product.price
        if save_count > 0:
            Discount._sum_describe.append(u"名称：{0}，数量：{1}".format(product.name, save_count))
        return total_price, save_price, u"小计：%.2f（元）" % total_price


class Discount95(Discount):
    def out(self, product, count):
        original_price = product.price * count
        total_price = original_price * 0.95
        save_price = original_price - total_price
        return total_price, save_price, u"小计：%.2f（元），节省%.2f（元）" % (total_price, save_price)

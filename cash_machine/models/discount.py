# -*- coding: utf-8 -*-
import copy


class Discount(object):
    def out(self, product, count):
        raise NotImplementedError()

    @staticmethod
    def summarize():
        raise NotImplementedError()


class NoDiscount(Discount):
    def out(self, product, count):
        total_price = count * product.price
        save_price = 0
        return total_price, save_price, u"小计：%.2f（元）" % total_price

    @staticmethod
    def summarize():
        return None


class Buy2Save1(Discount):
    __sum_describe = []

    def out(self, product, count):
        assert count > 0
        save_count = count / 3
        total_price = (count - save_count) * product.price
        save_price = save_count * product.price
        if save_count > 0:
            Buy2Save1.__sum_describe.append(u"名称：{0}，数量：{1}".format(product.name, save_count))
        return total_price, save_price, u"小计：%.2f（元）" % total_price

    @staticmethod
    def summarize():
        if len(Buy2Save1.__sum_describe) == 0:
            return None
        Buy2Save1.__sum_describe[0:0] = [u"买二赠一商品："]
        result = copy.deepcopy(Buy2Save1.__sum_describe)
        Buy2Save1.__sum_describe = []
        return result


class Discount95(Discount):
    def out(self, product, count):
        original_price = product.price * count
        total_price = original_price * 0.95
        save_price = original_price - total_price
        return total_price, save_price, u"小计：%.2f（元），节省%.2f（元）" % (total_price, save_price)

    @staticmethod
    def summarize():
        return None

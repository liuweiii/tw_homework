# -*- coding: utf-8 -*-
class Discount(object):
    def out(self, product, count):
        raise NotImplementedError()


class NoDiscount(Discount):
    def out(self, product, count):
        total_price = count * product.price
        save_price = 0
        return total_price, save_price, u"小计：%.2f（元）" % total_price


class Buy2Free1(Discount):
    def out(self, product, count):
        assert count > 0
        free_count = count / 3
        total_price = (count - free_count) * product.price
        save_price = free_count * product.price
        return total_price, save_price, u"小计：%.2f（元）" % total_price


class Discount95(Discount):
    def out(self, product, count):
        original_price = product.price * count
        total_price = original_price * 0.95
        save_price = original_price - total_price
        return total_price, save_price, u"小计：%.2f（元），节省%.2f（元）" % (total_price, save_price)

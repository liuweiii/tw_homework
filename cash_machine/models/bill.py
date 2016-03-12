class Bill(object):
    def __init__(self, products_describe, total_price, save_total_price):
        self.products_describe = products_describe
        self.save_total_price = save_total_price
        self.total_price = total_price

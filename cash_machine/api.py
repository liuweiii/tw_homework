# -*- coding: utf-8 -*-
from flask import Flask
from flask import request, render_template
from models.discount import Discount
from services.cash_machine_service import generate_bill, get_products
from models.product import Product

app = Flask(__name__)


@app.route("/", methods=["GET"])
def input_shop_list():
    return render_template("index.html", show="INPUT")


@app.route("/", methods=["POST"])
def process_shop_list():
    succeed, detail = generate_bill(request.form["shop_list"].replace('\'', '"'))
    if succeed:
        bill = detail
        return render_template("index.html", show="RESULT", products_describe=bill.products_describe,
                               total_price=bill.total_price, save_total_price=bill.save_total_price,
                               discount_sum=Discount.summarize())
    else:
        return render_template("index.html", show="ERROR", message=detail)


@app.route("/setting/", methods=["GET"])
def input_discount():
    products = get_products()
    return render_template("setting.html", products=products)


@app.route("/setting/", methods=["POST"])
def setting_discount():
    def __format_code_discounts():
        code_discounts_ = dict()
        for items in request.form:
            code, discount_string = items.split(".")
            discount = Discount.from_string(discount_string)
            if code not in code_discounts_:
                code_discounts_[code] = [discount]
            code_discounts_[code].append(discount)
        return code_discounts_

    code_discounts = __format_code_discounts()
    Product.reset_products()

    for item in code_discounts:
        product = Product.get_by_code(item)
        product.set_discounts(code_discounts[item])
    return render_template("setting.html", products=get_products())

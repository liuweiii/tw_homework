# -*- coding: utf-8 -*-
from flask import Flask
from flask import request, render_template
from models.discount import Discount
from services.cash_machine_service import generate_bill, get_products, set_discount


app = Flask(__name__)


@app.route("/", methods=["GET"])
def input_shop_list():
    return render_template("index.html", show="INPUT")


def print_sys_out(bill, discount_sum):
    try:
        products_describe = "\n".join(bill.products_describe)
        discount_sum = "" if discount_sum is None else "\n".join(discount_sum) + "\n----------------------\n"
        save_total = "" if bill.save_total_price is None else u"节省：{0}（元）\n".format(bill.save_total_price)
        out = u"""***<没钱赚商店>购物清单***\n""" \
              u"""{0}""" \
              u"""\n----------------------\n""" \
              u"""{1}""" \
              u"""总计：{2}（元）""" \
              u"""{3}""" \
              u"""**********************""".format(products_describe, discount_sum, bill.total_price, save_total)
        print out
    except Exception as e:
        print e


@app.route("/", methods=["POST"])
def process_shop_list():
    succeed, detail = generate_bill(request.form["shop_list"].replace('\'', '"'))
    if succeed:
        bill = detail
        discount_sum = Discount.summarize()
        print_sys_out(bill, discount_sum)
        return render_template("index.html", show="RESULT", products_describe=bill.products_describe,
                               total_price=bill.total_price, save_total_price=bill.save_total_price,
                               discount_sum=discount_sum)
    else:
        return render_template("index.html", show="ERROR", message=detail)


@app.route("/setting/", methods=["GET"])
def input_discount():
    return render_template("setting.html", products=get_products())


@app.route("/setting/", methods=["POST"])
def setting_discount():
    set_discount(request.form)
    return render_template("setting.html", products=get_products())

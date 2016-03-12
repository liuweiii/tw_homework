# -*- coding: utf-8 -*-
from flask import Flask
from flask import request, render_template
from services.cash_machine_service import to_bill_list
from common.exception import ProductNotFoundException
from models.discount import Discount
import json

app = Flask(__name__)


def render_out(bill_list):
    out = []
    total = 0
    save = 0
    for key in bill_list.keys():
        product = bill_list[key][0]
        count = bill_list[key][1]
        this_product_total, this_product_save, this_product_total_describe = product.discount(count)
        total += this_product_total
        save += this_product_save
        out.append(u"名称：%s，数量：%d %s，单价：%.2f（元），%s" %
                   (product.name, count, product.unit, product.price, this_product_total_describe))
    return out, total, save


@app.route("/", methods=["GET"])
def input_bill():
    return render_template("index.html", show="INPUT")


@app.route("/", methods=["POST"])
def process_bill():
    def _show_error(message=u"输入参数有误"):
        return render_template("index.html", show="ERROR", message=message)

    def _parse_shop_list():
        return json.loads(request.form["shop_list"].replace('\'', '"'))

    try:
        shop_list = _parse_shop_list()
        bill_list = to_bill_list(shop_list)
        out, total, save = render_out(bill_list)
        return render_template("index.html", show="RESULT", out=out, total=total, save=save,
                               discount_sum=Discount.summarize())
    except ValueError:
        return _show_error()
    except ProductNotFoundException:
        return _show_error(u"输入的条形码找不到对应商品")
    except Exception as e:
        return _show_error(u"这个错误[{0}]没被考虑到... ...".format(e.message))

# -*- coding: utf-8 -*-
from flask import Flask
from flask import request, render_template
from models.discount import Discount
from services.cash_machine_service import generate_bill


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

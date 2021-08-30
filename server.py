from flask import Flask, render_template, abort, request
import json

from pymongo import cursor, results
from data import data
from flask_cors import CORS
from config import db, parse_json


app = Flask(__name__)  # create a flask app
CORS(app)

me = {
    "name": "Chris",
    "last_name": "Daming",
    "age": 36,
    "email": "chris@legalgps.com",
    "address": {
        "street": "Atalanta",
        "number": 307
    }
}


@app.route('/')
@app.route('/home')
def home_page():
    return render_template("index.html")


@app.route("/about")
def about_me():
    return me["name"] + " " + me["last_name"]

# /about/email


@app.route("/about/email")
def about_me_email():
    return me["email"]


@app.route("/api/catalog")
def get_catalog():
    cursor = db.products.find({})
    prods = [ prod for prod in cursor]
    # prods = []
    # for prod in cursor:
    #     prods.append(prod)

    return parse_json(prods)

# If you want just the product title, do this:     prods = [ prod["title"] for prod in cursor]



@app.route("/api/catalog", methods=['POST'])
def save_product():
    product = request.get_json()

    if not "title" in product:
        return parse_json({"error": "title is required", "success": False })

    if not "price" in product or not product["price"]:
        return parse_json({"error": "price is required, and shouldn't be zero", "success": False })

    db.products.insert_one(product)
    return parse_json(product)



@app.route("/api/couponCodes/<code>")
def get_coupon(code):
    code = db.couponCodes.find_one({"code": code})
    return parse_json(code)

    

@app.route("/api/couponCodes")
def get_coupons():
    cursor = db.couponCodes.find({})
    codes = [code for code in cursor]
    return parse_json(codes)
    
    



@app.route("/api/couponCodes", methods=["POST"])
def save_coupon():
    coupon = request.get_json()

    if not "code" in coupon:
        return parse_json({"error": "code is required", "success": False})

    if not "discount" in coupon or not coupon["discount"]:
        return parse_json({"error": "discount is required, and shouldn't be zero", "success": False})

    db.couponCodes.insert_one(coupon)
    return parse_json(coupon)
    # data = request.get.data()
    # print(data)
    # print(type(data))

@app.route("/api/categories")
def get_categories():
    cursor = db.products.find({})
    categories = []
    for item in cursor:
        cat = item["category"]

        if cat not in categories:
            categories.append(cat)

    return parse_json(categories)

# Get the unique categories from the catalog (data var)
# and return them as a list of strings

# declare wtih greater/lower


@app.route("/api/catalog/id/<id>")
def get_product_by_id(id):
    for item in data:
        if(str(item["_id"]) == id):
            return parse_json(item)

    abort(404)
    # if id not in item["_id"]:
    #     print("Error. {id} does not exist")

    # else
    #     return json.dumps(_id)


@app.route("/api/catalog/category/<category>")
def get_products_by_category(category):
    cursor = db.products.find({"category": category})
    results = [prod for prod in cursor]
    return parse_json(results)


    # results = []
    # for item in data:
    #     if(item["category"].lower() == category.lower()):
    #         results.append(item)

    # return parse_json(results)


@app.route("/api/catalog/cheapest")
def get_cheapest():
    cheapest = data[0]
    for item in data:
        if(item["price"] < cheapest["price"]):
            cheapest = item

    return parse_json(cheapest)



@app.route("/api/test/populatedb")
def populate_db():
    for prod in data:
        db.products.insert_one(prod)

    return "Data loaded"


if __name__ == '__main__':
    app.run(debug=True)

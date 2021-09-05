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

@app.route("/about/email")
def about_me_email():
    return me["email"]


@app.route("/api/catalog")
def get_catalog():
    cursor = db.products.find({})
    prods = [ prod for prod in cursor]

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





@app.route("/api/catalog/id/<id>")
def get_product_by_id(id):
    product = db.products.find_one({"_id": id})
    if not product:
        abort(404)

    return parse_json(product)

  

@app.route("/api/catalog/category/<category>")
def get_products_by_category(category):
    cursor = db.products.find({"category": category})
    results = [prod for prod in cursor]
    return parse_json(results)



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


# """
# ####################ORDERS LOGIN#############################
# """




@app.route("/api/orders", methods=["post"])
def save_order():
    order = request.get_json()

    prods = order["products"]
    count = len(prods)
    if(count < 1):
        abort(400, "Error: Order without products are not allowed")

    for item in prods:
        id = item["_id"]
        print(id)

        db_item = db.products.find_one({"_id": id})
        item["price"] = db_item["price"]
        total += db_item["price"] * item["quantity"]

    print("The total is: ", total)
    order["total"] = total

    if "couponCode" in order and order["couponCode"]:

        code = order["couponCode"]
        coupon = db.couponCodes.find_one({"code": code})
        if coupon:
            discount = coupon["discount"]
            total = total - (total * discount) / 100
            order["total"] = total
        else:
            order["couponCode"] = "INVALID"
    

    db.orders.insert_one(order)
    return parse_json(order)


@app.route("/api/orders")
def get_orders():
    cursor = db.orders.find({})
    order = [ order for order in cursor]
    return parse_json(orders)


@app.route("/api/orders/<int:userId>")
def get_order_for_user(userId):
    cursor = db.orders.find({"userId": userId})
    order = [ order for order in cursor]
    return parse_json(orders)





# if __name__ == '__main__':
#     app.run(debug=True)



# START TESTING-----------------------------------------------


# @app.route("/api/cart/purchaseOrder/<order>")
# def get_order(order):
#     code = db.purchaseOrder.find_one({"order": order})
#     return parse_json()

# @app.route("/api/cart/purchaseOrder")
# def get_orders():
#      cursor = db.purchaseOrder.find({})
#      orders = [order for order in cursor]
#      return parse_json(orders)


# @app.route("/api/cart/purchaseOrder", methods=["POST"])
# def save_order():
#     order = request.get_json()
  

#     db.purchaseOrder.insert_one(order)
#     return parse_json(order)


# END TESTING----------------------------------------------------
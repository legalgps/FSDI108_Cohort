from flask import Flask, render_template, abort, request
import json
from data import data


app = Flask(__name__)  # create a flask app

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
    return json.dumps(data)


@app.route("/api/catalog", methods=['POST'])
def save_product():
    product = request.get_json()
    data.append(product)

    # data = request.get.data()
    # print(data)
    # print(type(data))

    return "Ok"


@app.route("/api/categories")
def get_categories():
    categories = []
    for item in data:
        cat = item["category"]

        if cat not in categories:
            categories.append(cat)

    return json.dumps(categories)

# Get the unique categories from the catalog (data var)
# and return them as a list of strings

# declare wtih greater/lower


@app.route("/api/catalog/id/<id>")
def get_product_by_id(id):
    for item in data:
        if(item["_id"] == id):
            return json.dumps(item)

    abort(404)
    # if id not in item["_id"]:
    #     print("Error. {id} does not exist")

    # else
    #     return json.dumps(_id)


@app.route("/api/catalog/category/<category>")
def get_products_by_category(category):
    results = []
    for item in data:
        if(item["category"].lower() == category.lower()):
            results.append(item)

    return json.dumps(results)


@app.route("/api/catalog/cheapest")
def get_cheapest():
    cheapest = data[0]
    for item in data:
        if(item["price"] < cheapest["price"]):
            cheapest = item

    return json.dumps(cheapest)


# def get_cheapest_price():


#     min_price = []
#     for item in data:
#         priced = item[price]

#         if priced not in min_price:
#             min_price.append(priced)

#     return json.dumps(min(min_price))


if __name__ == '__main__':
    app.run(debug=True)

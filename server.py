from flask import Flask, render_template
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


if __name__ == '__main__':
    app.run(debug=True)

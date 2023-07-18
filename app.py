from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# app init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
        )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


#  Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "quantity")


#  Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create the Tables
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def get():
    return jsonify({
            'Url Routes':{
                "home-GET": "/",
                "get all product-GET": "Product",
                "add a product-POST": "Product",
                "get a product detail-GET":"Product/id",
                "edit a product detail-PUT":"Product/id",
                "delete a product-DELETE":"Product/id"
            },
            })


# add product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    new_product = Product(name, description, price, quantity)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# get all product
@app.route("/product", methods=["GET"])
def get_products():
    products = Product.query.all()
    result = products_schema.dump(products)
    return result


# get single product
@app.route("/product/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    result = product_schema.dump(product)
    return result


# edit a product
@app.route("/product/<int:id>", methods=["PUT"])
def edit_product(id):
    product = Product.query.get(id)

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    product.name = name
    product.price = price
    product.description = description
    product.quantity = quantity

    db.session.commit()

    return product_schema.jsonify(product)


# delete a product
@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return {"msg": "product deleted"}


# Run Server
if __name__ == "__main__":
    app.run(debug=True)

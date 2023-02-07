from flask import Flask, Response, request
from services.product import productService

app = Flask(__name__)
products = productService()


@app.route("/")
def api_docs():
    return """<p>Shopping Cart API</p> 
    <ul>
    <li>/products - GET, POST, DELETE</li>
    <li>/filtered-products - GET</li>
    <li>/products-csv - GET</li>
    </ul>"""


@app.route("/products")
def get_products():
    return products.get()


@app.route("/filtered-products")
def get_products_by():
    return products.get_by(request.json)


@app.post("/products")
def add_product():
    return products.add(request.json)


@app.delete("/products/<id>")
def remove_product(id):
    return Response(products.remove(id), status=202, mimetype='application/json')


@app.route("/products-csv")
def get_products_csv():
    return products.get_csv()

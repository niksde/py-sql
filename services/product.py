import pymysql
from flask import make_response, Response
import io
import csv
import json
from services.utils import map_to_object


class productService:
    global cursor
    global con

    def __init__(self):
        self.con = pymysql.connect(host='localhost', user='root',
                                   password='test', port=3306)
        self.cursor = self.con.cursor()
        self.cursor.execute("USE shoppingCart")

    def __get_products(self):
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        column = [t[0] for t in self.cursor.description]
        return column, rows

    def get(self):
        column, rows = self.__get_products()
        products = []
        for row in rows:
            product = {}
            for i, value in enumerate(row):
                product[column[i]] = value
            products.append(product)
        return json.dumps(products, indent=3)

    def get_by(self, content):
        query = "SELECT * FROM products WHERE title=%s and variant_sku=%s"
        values = (content["title"], content["sku"])
        self.cursor.execute(query, values)
        row = self.cursor.fetchone()
        column = [t[0] for t in self.cursor.description]

        product = {}
        for i, value in enumerate(row):
            product[column[i]] = value
        return json.dumps(product, indent=3)

    def add(self, content):
        keys, values, types = map_to_object(content)
        query = f'INSERT INTO products ({", ".join(keys)}) VALUES ({", ".join(types)})'

        self.cursor.execute(query, tuple(values))
        self.con.commit()
        return Response('created', status=201, mimetype='application/json')

    def remove(self, id):
        self.cursor.execute("DELETE FROM products WHERE id=%s", (id))
        self.con.commit()
        return 'removed'

    def get_csv(self):
        si = io.StringIO()
        cw = csv.writer(si)
        column, rows = self.__get_products()
        csvList = [column, *rows]
        cw.writerows(csvList)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=products.csv"
        output.headers["Content-type"] = "text/csv"
        return output

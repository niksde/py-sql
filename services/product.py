# import pymysql
from flask import make_response
import io
import csv


class productService:
    global cursor

    def __int__(self):
        # con = pymysql.connect(host='localhost', user='root', password='test', port=3306)
        # self.cursor = con.cursor()
        ""

    def get(self):
        return 'products'

    def get_by(self):
        return 'by'

    def add(self):
        return 'created'

    def remove(self):
        return 'removed'

    def get_csv(self):
        si = io.StringIO()
        cw = csv.writer(si)
        csvList = [
            ["Test", "Data"],
            ["True", 1.1],
            ["False", 2.2]
        ]
        cw.writerows(csvList)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

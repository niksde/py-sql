import pymysql
import os
import json

# read JSON file
filePath = os.path.abspath('.') + "/csvjson.json"
json_data = open(filePath).read()
json_obj = json.loads(json_data)


# do validation and checks before insert
def validate_string(val):
    if val != None:
        if type(val) is int:
            return str(val).encode('utf-8')
        else:
            return val


# connect to MySQL
con = pymysql.connect(host='localhost', user='root', password='test', port=3306)
cursor = con.cursor()

# create db/table if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS shoppingCart")
cursor.execute("USE shoppingCart")
cursor.execute("CREATE TABLE IF NOT EXISTS products(id int NOT NULL AUTO_INCREMENT, PRIMARY KEY (id),  handle text, title text, body text, vendor varchar(50), type varchar(50), tags text, option1_name varchar(50), option1_value varchar(50), option2_name varchar(50), option2_value varchar(50), option3_name varchar(50), option3_value varchar(50), variant_sku varchar(50), variant_grams varchar(50), variant_inventory_tracker varchar(50), variant_inventory_qty varchar(50), variant_inventory_policy varchar(50), variant_fulfillment_service varchar(50), variant_price varchar(50), variant_compare_at_price varchar(50), image_src text)")


def map_to_object(obj):
    keys = []
    values = []
    types = []
    for key, value in obj.items():
        keys.append(key.replace(" ", "_").lower())
        values.append(validate_string(value))
        types.append("%s")
    return keys, values, types


# parse json data to SQL insert
for i, item in enumerate(json_obj):
    keys, values, types = map_to_object(item)
    query = f'INSERT INTO products ({", ".join(keys)}) VALUES ({", ".join(types)})'

    cursor.execute(query, tuple(values))
con.commit()
con.close()

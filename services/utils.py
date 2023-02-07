
def validate_string(val):
    if val != None:
        if type(val) is int:
            return str(val).encode('utf-8')
        else:
            return val


def map_to_object(obj):
    keys = []
    values = []
    types = []
    for key, value in obj.items():
        keys.append(key.replace(" ", "_").lower())
        values.append(validate_string(value))
        types.append("%s")
    return keys, values, types

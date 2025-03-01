def verify(data, schema):
    for name, type_ in schema.items():
        if name not in data:
            return False
        if not isinstance(data[name], type_):
            return False
    return True



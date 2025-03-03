from .login_flow import tokens

def verify(data, schema):
    for name, type_ in schema.items():
        if name not in data:
            return False
        if not isinstance(data[name], type_):
            return False
    return True


def is_valid_token(token: str) -> bool:
    return token in tokens

def get_user_id(token: str) -> str:
    name, _id = tokens[token]
    return _id

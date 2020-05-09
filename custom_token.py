import jwt

def func_create_custom_token(payload):

    token=jwt.encode(payload, "dont tell anyone")
    token = token.decode("utf-8")
    return token

def func_decode_custom_token(encode_token):

    payload = jwt.decode(encode_token, "dont tell anyone")
    print(1,payload)
    return payload

def func_compare_token(to_token, from_token):

    if to_token == from_token:
        return True
    else:
        return False     




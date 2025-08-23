from authlib.jose import jwt


def encrypt_data(data: dict, secret_key: str) -> str:
    """Encrypt data using JWT"""
    token = jwt.encode({"alg": "HS256"}, data, secret_key)
    return token.decode("utf-8")


def decrypt_data(token: str, secret_key: str) -> dict:
    """Decrypt data using JWT"""
    data = jwt.decode(token, secret_key)
    return data

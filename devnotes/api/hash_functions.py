from hashlib import md5


def get_hash(string: str) -> str:
    return md5(string.encode('UTF-8')).hexdigest()

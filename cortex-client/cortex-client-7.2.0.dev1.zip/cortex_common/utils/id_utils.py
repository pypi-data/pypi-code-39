import hashlib

__all__ = [
    "hash_query",
]

def hash_query(query):
    return hashlib.md5("".join(query.lower().split()).encode('utf-8')).hexdigest()
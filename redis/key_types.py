from enum import Enum


class KeyCacheProp(Enum):
    DEFAULT = 1,
    WRITE_ONCE = 2


"""
Currently supported commands with WRITE_ONCE:
    GET,
    HGET,
    HGETALL,
    HMGET,
"""


# For now we only support single level key prefixes
# dict [key_prefix (str) -> KeyCacheProp]
def get_key_type(key: str, key_types):
    prefix = key.split(":")[0]
    return key_types.get(prefix, KeyCacheProp.DEFAULT)

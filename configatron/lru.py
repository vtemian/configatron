import time
from collections import OrderedDict
from typing import Optional


class LRUCache:
    def __init__(self, capacity: int, lifetime: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.lifetime = lifetime

    def get(self, key: tuple) -> Optional[object]:
        if key not in self.cache:
            return None

        item, added = self.cache[key]
        if time.time() - added > self.lifetime:
            self.cache.move_to_end(key)
            return item

        del self.cache[key]
        return None

    def put(self, key: tuple, value: object) -> None:
        self.cache[key] = (value, time.time())
        self.cache.move_to_end(key)

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def purge(self):
        self.cache = OrderedDict()

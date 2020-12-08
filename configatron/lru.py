import time
from collections import OrderedDict
from typing import Optional


class LRUCache:
    def __init__(self, capacity: int, lifetime: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.lifetime = lifetime

    def get(self, key: str) -> Optional[object]:
        """
        Return an object from cache, based on a cache key.
        If the object lifetime is smaller than the constraint, remove it.

        :param key: uniq cache key, identifying an object within the cache.
        :return: object or None
        """

        if key not in self.cache:
            return None

        item, added = self.cache[key]
        if time.time() - added < self.lifetime:
            self.cache.move_to_end(key)
            return item

        del self.cache[key]
        return None

    def put(self, key: str, value: object):
        """
        Add an item to the internal cache. Move it to the end and upadte capacity.

        :param key: uniq cache key, identifying an object within the cache.
        :param value: object to cache.
        :return: None
        """

        self.cache[key] = (value, time.time())
        self.cache.move_to_end(key)

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def purge(self):
        """
        Remove all items from cache, by initializing a new cache.
        :return: None
        """

        self.cache = OrderedDict()

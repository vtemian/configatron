from typing import Dict, Union

from .index import Index
from .lru import LRUCache
from .nodes.group import Group
from .utils import EmptyConfig


DEFAULT_CACHE_OPTIONS = {
    "size": 100,
    "lifespan": 10
}


class Configatron:
    def __init__(self, source: str, cache_options: Dict[str, str] = None):
        self.index = Index(source)

        if cache_options is None:
            cache_options = DEFAULT_CACHE_OPTIONS

        cache_options = {**DEFAULT_CACHE_OPTIONS, **cache_options}
        self.lru = LRUCache(cache_options["size"], cache_options["lifespan"])

    def get(self, group_name: str) -> Union[Group, EmptyConfig]:
        # Get group from cache. LRU also handles expired items.
        group = self.lru.get((group_name, ))  # type: Optional[Group]
        if group:
            return group

        # Group may be newly added to the file or its configuration have been updated, so we can re-index.
        group = self.index.get(group_name)
        if not group or not group.is_fresh:
            self.index.build()

            # If the group was deleted, return an infinite empty dict.
            group = self.index.get(group_name)
            if not group:
                return EmptyConfig()

        self.lru.put((group.name, ), group)

        return group

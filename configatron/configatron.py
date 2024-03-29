from typing import Dict, Union, List

from .index import Index
from .lru import LRUCache
from .nodes.group import Group
from .utils import EmptyConfig


DEFAULT_CACHE_OPTIONS = {
    "size": 10000,  # number of items in cache, default 10 000 items
    "lifespan": 60 * 60,  # seconds for each item in cache, default 1h
}


class Configatron:
    def __init__(
        self, source: str, overrides: List[str] = None, cache_options: Dict[str, str] = None, validate: bool = True
    ):
        """
        Instantiate the two main components: index and LRU cache.
        Build the initial index and validate the file's syntax.

        :param source: Path to config file.
        :param overrides: Some properties can be overwritten, based on specific overrides.
        :param cache_options: Configure cache's size and lifespan.
        :param validate: Throw exception if the syntax of the config file is not valid.
        """

        if overrides:
            overrides = overrides[::-1]

        self.index = Index(source, overrides)

        if cache_options is None:
            cache_options = DEFAULT_CACHE_OPTIONS

        self.cache_options = {**DEFAULT_CACHE_OPTIONS, **cache_options}
        self.lru = LRUCache(self.cache_options["size"], self.cache_options["lifespan"])

        # build the initial index and validate the config as well
        if validate:
            self.index.build(True)

    def get(self, group_name: str) -> Union[Group, EmptyConfig]:
        """
        Return a configuration group.

        Search in the local LRU cache for it. If missing, try to retrieve it from the index.
        Re-index if the group was updated offline or if the group is not in the index.
        If found, update cache. Otherwise, return an EmptyConfig.

        :param group_name:
        :return: Group or EmptyConfig
        """

        # Get group from cache. LRU also handles expired items.
        group = self.lru.get(group_name)  # type: Optional[Group]
        if group:
            return group

        # Group may be newly added to the file or its configuration have been updated, so we can re-index.
        group = self.index.get(group_name)
        if not group or not group.is_fresh:
            self.index.build()

            # Purge the entire cache if the file was re-indexed
            self.lru.purge()

            # If the group was deleted, return an infinite empty dict.
            group = self.index.get(group_name)
            if not group:
                return EmptyConfig()

        self.lru.put(group.name, group)

        return group

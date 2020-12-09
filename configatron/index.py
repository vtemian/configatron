import hashlib
import logging
from typing import Optional, List

from configatron.errors import ValidationError
from configatron.nodes.group import Group
from configatron.reader import Reader
from configatron.scanner import Scanner


class Index:
    def __init__(self, source: str, overrides: List[str] = None):
        # Config source, filepath.
        self.source = source

        # Keep the source's last modified time so we don't need to re-index the file if it hasn't changed.
        self.source_cache_key = None

        # Current groups index. It maps the group's name to it's (start byte, end byte, content sha)
        self.groups_index = {}

        self.scanner = Scanner(Reader(source), overrides)

    def _compute_source_key(self) -> str:
        """
        Compute a blake2b hash over source's content.

        :return: Source's content hash.
        """
        _hash = hashlib.blake2b()

        with open(self.source, "rb") as f:
            while chunk := f.read(8192):
                _hash.update(chunk)

        return _hash.hexdigest()

    def _should_index(self):
        """
        Indexing the entire file can be really costly. We want to avoid this operation as much as possible.
        """

        return self.source_cache_key != self._compute_source_key()

    def build(self, validate: bool = False):
        """
        Parse the entire file and index groups. Store group name as key and a tuple
         (start byte, end byte and content sha)
        as value.

        :param validate: raise validation errors if we find invalid configurations.
        """

        if not self._should_index():
            logging.debug(f"Nothing to index for {self.source}.")
            return

        self.groups_index = {}

        for group in self.scanner.groups(validate):
            if validate and group.name in self.groups_index:
                raise ValidationError(f"Duplicate group name: {group.name}")

            self.groups_index[group.name] = group

        self.source_cache_key = self._compute_source_key()

    def get(self, group_name: str) -> Optional[Group]:
        """
        Get a group from index

        :param group_name:
        :return: Group or None
        """

        return self.groups_index.get(group_name)

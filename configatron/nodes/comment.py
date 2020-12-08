import re

from .base import Node


class Comment(Node):
    """
    starts with
                new line
                  or
             any number spaces
                    followed by `;` and any character
    end
    """

    REGEX = re.compile("^(\n)|(\s*(;.*)?)$")

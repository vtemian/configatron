class EmptyConfig(dict):
    """
    Empty dict that for `.get()` it always returns itself.
    """

    def get(self, name):
        return EmptyConfig()

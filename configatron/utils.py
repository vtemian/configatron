class EmptyConfig(dict):
    def get(self, name):
        return EmptyConfig()

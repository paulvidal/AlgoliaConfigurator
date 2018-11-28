class AlgoliaSetting:

    def __init__(self, name, settings=None, default=None):
        self.name = name
        self.value = settings.get(name) if settings and settings.get(name) else default

    def add_itself_to_settings(self, settings):
        if self.value is not None:
            settings[self.name] = self.value

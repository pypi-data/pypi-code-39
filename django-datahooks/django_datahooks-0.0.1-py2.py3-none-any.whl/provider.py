class DataProvider:
    def add_arguments(self, parser):
        pass

    def run(self, **options):
        raise NotImplementedError()

class SQLAdapter:
    def __new__(cls, connector, **kwargs):
        return connector(**kwargs)

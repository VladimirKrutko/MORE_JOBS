class StaticMeta(type):
    def __new__(cls, name, bases, dct):
        for attr, value in dct.items():
            if callable(value):
                dct[attr] = staticmethod(value)
        return super().__new__(cls, name, bases, dct)
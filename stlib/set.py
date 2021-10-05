class Fake(object):

    def __getitem__(self, item):
        print("__getitem__ called", item)

    def __delitem__(self, key):
        print('__delitem__ called', key)

    def __setitem__(self, key, value):
        print('__setitem__ called', key, value)

    def __len__(self):
        print('__len__ called')
        return 0


a = Fake()
a[0]  # __getitem__ called
a[0] = 1  # __setitem__ called
del a[0]  # __delitem__ called
len(a)  # __len__ called


class Demo(object):
    name = "demo"

    def __new__(cls, *args, **kwargs):
        print("args: ", args, "kwargs: ", kwargs)
        print("do something before obj created")
        obj = super(Demo, cls).__new__(cls)
        print("do something after obj created")
        return obj

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        print("__del__ called")


class AttrDemo(object):
    name = "attrdemo"
    @property
    def t(self):
        pass
    def __getattr__(self, item):
        print(item)
        pass

    # def __getattribute__(self, item):
    #     print(self.name)
    #
    # def __setattr__(self, key, value):
    #     setattr(self, "key", value)
    #
    # def __delattr__(self, item):
    #     pass

import types


class Monkey(object):

    def say_hello(self):
        print("hello monkey")


def say_hello(self):
    print("hello pig")


def say_something(self):
    print("say something")


class Test(object):

    def __init__(self):
        self.data = 1

    def __next__(self):
        if self.data >= 6:
            raise StopIteration
        self.data += 1
        return self.data

    def __iter__(self):
        return self


obj = Test()
from collections import Iterable

isinstance(obj, Iterable)


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def test():
    for x in range(10):
        yield 10


if __name__ == "__main__":
    monkey = Monkey()
    monkey.say_hello()

    # 替换掉say hello
    Monkey.say_hello = say_hello
    pig = Monkey()
    pig.say_hello()

    m = Monkey()
    m.say_hello = types.MethodType(say_something, m)
    m.say_hello()

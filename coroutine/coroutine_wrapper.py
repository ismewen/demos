import functools
import inspect

from coroutine.yield_loop import YieldLoop


class CoroutineWrapper(object):

    def __init__(self, loop, gen):
        self.loop = loop
        self.gen = gen
        self.context = None  # 上下文

    def send(self, value):
        value = self.gen.send(value)
        self.context = value
        # 重新加入到 可执行队列
        self.loop.add_coroutine(self)

    def __next__(self):
        value = next(self.gen)
        self.context = value

    def throw(self, tp, *rest):
        return self.gen.throw(tp, *rest)

    def close(self):
        return self.gen.close()

    def __getattr__(self, item):
        #
        return getattr(self.gen, item)


def coroutinewp(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        if inspect.isgenerator(gen):
            core = CoroutineWrapper(YieldLoop.instance(), gen)
            return core
        else:
            raise RuntimeError("type({}) is not support".format(type(gen)))

    return wrapper

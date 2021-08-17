import abc

import arrow


class Image(abc.ABC):

    @abc.abstractmethod
    def display(self):
        pass


class RealImage(Image):

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.load_image_form_disk()

    def display(self):
        print("Displaying %s" % self.file_name)

    def load_image_form_disk(self):
        print("Load %s from disk" % self.file_name)


class ProxyImage(Image):

    def __init__(self, file_name):
        self.file_name = file_name
        self.image = None

    def display(self):
        if not self.image:
            self.image = RealImage(self.file_name)
        self.image.display()


ThirdImage = RealImage


class ThirdProxyImage(ThirdImage):

    def __init__(self, file_name):
        self.file_name = file_name
        self.origin_obj = None

    def display(self):
        if not self.origin_obj:
            origin_obj = ThirdImage(file_name=self.file_name)
            self.origin_obj = origin_obj
        return self.origin_obj.display()


class ProxyBase(object):

    def __init__(self, method):
        self.method = method
        self.g = dict()

    def __call__(self, *args, **kwargs):
        self.before_start()
        res = None
        if self.can_carried_out():
            res = self.method(*args, **kwargs)
            self.after_done()
        return res

    @abc.abstractmethod
    def before_start(self):
        pass

    def can_carried_out(self):
        return True

    @abc.abstractmethod
    def after_done(self):
        pass


class LoggerProxy(ProxyBase):

    def before_start(self):
        print("%s start" % self)

    def after_done(self):
        print("%s done" % self)


class TimerProxy(ProxyBase):

    def before_start(self):
        self.g["start"] = arrow.utcnow()

    def after_done(self):
        end = arrow.utcnow()
        spend = (end - self.g["start"]).total_seconds()
        print("run %s spend %s" % (self, spend))


class Proxy(object):

    def __init__(self, origin_cls, proxy_cls):
        self.origin_cls = origin_cls
        self.proxy_cls = proxy_cls
        self.origin_obj = None

    def __call__(self, *args, **kwargs):
        obj = self.origin_cls(*args, **kwargs)
        self.origin_obj = obj
        return self

    def __getattr__(self, item):
        r = getattr(self.origin_obj, item)
        if callable(r):
            return self.proxy_cls(r)
        return r


class ProxyFactory(object):

    def __init__(self, proxy_cls):
        self.proxy_cls = proxy_cls

    def __call__(self, origin_cls):
        return Proxy(origin_cls=origin_cls, proxy_cls=self.proxy_cls)


class Demo(object):

    def test(self):
        print("sleep 2 seconds")
        import time
        time.sleep(2)


if __name__ == "__main__":
    print("没有代理")
    Demo().test()
    print("logger代理")
    ProxyFactory(LoggerProxy)(Demo)().test()
    print("Timer 代理")
    ProxyFactory(TimerProxy)(Demo)().test()

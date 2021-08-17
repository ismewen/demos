import abc


class TargetInterface(abc.ABC):
    # 定义的一组接口

    @abc.abstractmethod
    def f1(self):
        pass

    @abc.abstractmethod
    def f2(self):
        pass

    @abc.abstractmethod
    def f3(self):
        pass


class Adaptee(object):
    # 不符合定义规范的一组接口
    def fa(self):
        pass

    def fb(self):
        pass

    def f3(self):
        pass


# 通过继承的方式实现Adapter
class AdapterByInherit(TargetInterface, Adaptee):

    def f1(self):
        return self.fa()

    def f2(self):
        return self.fb()


# 通过组合+委托的方式实现Adapter
class AdapterByCombination(object):

    def init(self, adaptee: Adaptee):
        self.adaptee = adaptee

    def f1(self):
        return self.adaptee.fa()

    def f2(self):
        return self.adaptee.fb()

    def f3(self):
        return self.adaptee.f3()


if __name__ == "__main__":
    a = AdapterByInherit()
    a.f1()
    a.f2()

    adaptee = Adaptee()
    b = AdapterByCombination(adaptee)
    b.f1()
    b.f2()
    b.f3()

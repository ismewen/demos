import abc
import typing


class Message(object):

    def __init__(self, msg):
        self.msg = msg


class Subject(abc.ABC):
    observers: typing.List['Observer'] = []

    def __init__(self):
        self.observers = []

    def register_observer(self, observer: 'Observer'):
        self.observers.append(observer)

    def remove_observer(self, observer: 'Observer'):
        self.observers.remove(observer)

    def notify_observers(self, message: 'Message'):
        for observer in self.observers:
            observer.update(message)


class Observer(abc.ABC):

    def update(self, message: 'Message'):
        pass


class XiaoMianYang(Observer):

    def update(self, message: 'Message'):
        print("小绵羊收到了信息: %s" % message.msg)
        print("小绵羊开始逃跑...")


class LieRen(Observer):

    def update(self, message: 'Message'):
        print("猎人收到了信息: %s" % message.msg)
        print("猎人开始打猎...")




if __name__ == "__main__":
    subject = Subject()
    message = Message("狼来了")
    suci = XiaoMianYang()
    lieren = LieRen()
    subject.register_observer(suci)
    subject.register_observer(lieren)
    subject.notify_observers(message=message)

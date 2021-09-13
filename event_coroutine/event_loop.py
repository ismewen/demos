import select
import socket
from collections import deque

from event_coroutine.future import Future
from event_coroutine.socket_wrapper import SocketWrapper


class EventLoop(object):
    coroutines = deque()
    current = None
    epoll = select.epoll()

    handlers = dict()

    @classmethod
    def get_instance(cls):
        if not cls.current:
            cls.current = EventLoop()
        return cls.current

    def create_future(self):
        return Future(loop=self)

    def create_listen_socket(self, ip="localhost", port=8999):
        sock = socket.socket()
        sock.bind((ip, port))
        sock.listen()
        return SocketWrapper(sock, loop=self)

    def register_handler(self, fileno, events, handler):
        self.handlers[fileno] = handler
        self.epoll.register(fileno, events)

    def unregister_handler(self, fileno):
        self.epoll.unregister(fileno)
        self.handlers.pop(fileno)

    def run_coroutine(self, coroutine):
        try:
            future = coroutine.send(None)
            future.set_coroutine(coroutine)
        except Exception as e:
            print(" coroutine run exception %s" % str(e))

    def run_forever(self):
        while True:
            while self.coroutines:
                self.run_coroutine(self.coroutines.popleft())
            events = self.epoll.poll(1)
            for fileno, event in events:
                # 获取回调
                handler = self.handlers.get(fileno)
                handler()

    def add_coroutine(self, co):
        self.coroutines.append(co)

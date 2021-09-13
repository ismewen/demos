import select

from event_coroutine.future import Future


class SocketWrapper(object):
    # 创建套接字->绑定->listen->recv

    def __init__(self, sock, loop):
        sock.setblocking(False)
        self.sock = sock
        self.loop = loop

    def fileno(self):
        return self.sock.fileno()

    async def accept(self):
        while True:
            try:
                sock, addr = self.sock.accept()
                return SocketWrapper(sock, loop=self.loop), addr
            except BlockingIOError:
                print("Blocking Error")
                print("create future")
                await self.create_future_for_events(select.EPOLLIN)

    async def recv(self, rv_length):
        while True:
            try:
                data = self.sock.recv(rv_length)
                return data
            except BlockingIOError:
                await self.create_future_for_events(select.EPOLLIN)

    async def send(self, data):
        while True:
            try:
                self.sock.send(data)
                return
            except BlockingIOError as e:
                await self.create_future_for_events(select.EPOLLOUT)

    def fileno(self):
        return self.sock.fileno()

    def create_future_for_events(self, events):
        future = self.loop.create_future()

        def handler():
            future.set_done()
            self.loop.unregister_handler(self.fileno())
            if future.coroutine:
                # 继续调度
                self.loop.add_coroutine(future.coroutine)

        future.loop.register_handler(self.fileno(), events, handler)

        return future

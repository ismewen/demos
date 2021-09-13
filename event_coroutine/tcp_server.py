from event_coroutine.event_loop import EventLoop


class TCPServer(object):

    def __init__(self, loop):
        self.loop = loop
        self.listen_sock = self.loop.create_listen_socket()
        self.loop.add_coroutine(self.server_forever())

    async def handle_client(self, sock):
        data = await sock.recv(1024)
        if not data:
            print("client disconnected")
        await sock.send(data.upper())

    async def server_forever(self):
        while True:
            print("look at here")
            sock, addr = await self.listen_sock.accept()
            print("client connect addr = {}".format(addr))
            self.loop.add_coroutine(self.handle_client(sock))


if __name__ == "__main__":
    loop = EventLoop.get_instance()
    server = TCPServer(loop)
    loop.run_forever()

class TCPServer(object):

    def __init__(self, loop):
        self.loop = loop
        self.listen_sock = self.loop.create_listen_socket()

    async def handle_client(self, sock):
        while True:
            data = await sock.acc


    async def server_forever(self):
        while True:
            sock, addr = await self.listen_sock.accept()
            print("client connect addr = {}".format(addr))
            self.loop.add_coroutine(self.handle_client(sock))

class Future(object):

    def __init__(self, loop):
        self.loop = loop
        self.done = False
        self.coroutine = None

    def set_coroutine(self, coroutine):
        self.coroutine = coroutine

    def set_done(self):
        self.done = True

    def result(self):
        pass

    # 如果没有完成任务，让出cpu
    def __await__(self):
        if not self.done:
            yield
        return

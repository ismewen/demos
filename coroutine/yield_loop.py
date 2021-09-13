from collections import deque


class YieldLoop(object):
    current = None
    coroutines = deque()

    @classmethod
    def instance(cls):
        if not cls.current:
            cls.current = YieldLoop()
        return cls.current

    def add_coroutine(self, coroutine):
        self.coroutines.append(coroutine)

    def run_coroutine(self, coroutine):
        try:
            print("what is context: ", coroutine.context)
            coroutine.send(coroutine.context)
        except StopIteration:
            print("coroutine stopped")

    def run_until_complete(self):
        while self.coroutines:
            coroutine = self.coroutines.popleft()
            self.run_coroutine(coroutine)

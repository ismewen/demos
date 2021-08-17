import abc


class HandleBase(abc.ABC):

    def __init__(self):
        self.should_pass = True

    def has_next(self):
        return self.next_handle is not None

    def set_next(self, next_handle: 'HandleBase'):
        self.next_handle = next_handle

    def handle(self, request):
        pass


class ProcessChain(object):

    def __init__(self):
        self.chain = []  # type []HandleBase

    def add_process(self, handle: HandleBase):
        self.chain.append(handle)

    def handle(self, request):
        for handle in self.chain:
            handle.handle(request)
            if not handle.should_pass:
                break


class ProcessA(HandleBase):

    def handle(self, request):
        print("ProcessA: a")


class ProcessB(HandleBase):
    def handle(self, request):
        print("ProcessB: b")


class ProcessC(HandleBase):
    def handle(self, request):
        print("ProcessC: c")


class ProcessD(HandleBase):

    def handle(self, request):
        print("ProcessD: d, 将会终端后续执行")
        self.should_pass = False


class ProcessE(HandleBase):
    def handle(self, request):
        print("ProcessE: e")


if __name__ == "__main__":
    process_chain = ProcessChain()
    process_chain.add_process(ProcessA())
    process_chain.add_process(ProcessB())
    process_chain.add_process(ProcessC())
    process_chain.add_process(ProcessD())
    process_chain.add_process(ProcessE())

    process_chain.handle("message")

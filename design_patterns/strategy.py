import abc


class Strategy(abc.ABC):

    def do_operation(self, a: int, b: int) -> int:
        pass


class AddStrategy(abc.ABC):

    def do_operation(self, a: int, b: int) -> int:
        return a + b


class SubStrategy(abc.ABC):

    def do_operation(self, a: int, b: int) -> int:
        return a - b


class MultiplyStrategy(abc.ABC):

    def do_operation(self, a, b):
        return a * b


class StrategyContext(object):

    def __init__(self, strategy: Strategy()):
        self.strategy = strategy

    def exec_strategy(self, a, b):
        return self.strategy.do_operation(a, b)


if __name__ == "__main__":
    print("1 + 1 = %s" % StrategyContext(AddStrategy()).exec_strategy(1, 1))
    print("1- 1 = %s" % StrategyContext(SubStrategy()).exec_strategy(1, 1))
    print("1 * 1 = %s" % StrategyContext(MultiplyStrategy()).exec_strategy(1, 1))

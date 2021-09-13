import asyncio
import time

from coroutine.coroutine_wrapper import coroutinewp
from coroutine.yield_loop import YieldLoop


@coroutinewp
def test_one():
    sum = 0
    for i in range(1, 100):
        print("yield %s" % i)
        sum += yield i
    print("sum = ", sum)


@coroutinewp
def producer(q):
    while True:
        print("producer start running")
        while len(q) > 0:
            # 交出cpu
            yield
        q.extend(["Goods" for x in range(5)])
        print("生产了 5 个 Goods")


@coroutinewp
def consumer(q):
    while True:
        if len(q) == 0:
            # 消费完了， 让出cpu给生产者执行
            yield
        while len(q):
            q.pop()
            # 一秒钟消费一个
            time.sleep(1)
            print("消费一个 good, 剩余: %s" % len(q))


def test_test_one():
    print("hello world")
    event_loop = YieldLoop.instance()
    event_loop.add_coroutine(test_one())
    event_loop.run_until_complete()
    print("all coroutine completed")


def test_consumer_producer(q):
    event_loop = YieldLoop.instance()
    event_loop.add_coroutine(producer(q))
    event_loop.add_coroutine(consumer(q))
    event_loop.run_until_complete()


if __name__ == "__main__":
    from collections import deque

    q = deque()
    test_consumer_producer(q)

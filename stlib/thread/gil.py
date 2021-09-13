import multiprocessing
import threading
import time


def complex_compute():
    i = 0
    while i < 1000000 * 100:
        i += 1


def sync_process():
    start = time.time()
    for x in range(10):
        complex_compute()
    end = time.time()
    print("sync spend %d" % int(end - start))


def async_thread():
    threads = []
    for x in range(10):
        t = threading.Thread(target=complex_compute)
        threads.append(t)
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.time()

    print("async thread spend %d" % int(end - start))


def test():
    # 开启两个进程，一个进程循环同步执行十次 `complex_compute`, 一个进程开启十个线程,每个线程执行一次 `complex_compute`
    syncp = multiprocessing.Process(target=sync_process)
    asyncp = multiprocessing.Process(target=async_thread)
    syncp.start()
    asyncp.start()

    syncp.join()
    asyncp.join()


if __name__ == "__main__":
    test()

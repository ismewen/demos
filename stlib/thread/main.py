# 初始化
# 提交任务
# 获取结果
import time
import threading
from concurrent.futures import ThreadPoolExecutor


def task():
    for i in range(2):
        print("this is a task, i={}, thread id={}".format(i, threading.get_native_id()))
        time.sleep(1)
    return "task"

# 初始化线程池

res = []

if __name__ == "__main__":
    tp = ThreadPoolExecutor(10)
    for i in range(10):
        res.append(tp.submit(task))
    for x in res:
        print(x.result())
# producer 和 consumer模型
import time

cnt = 0


def ethan():
    global cnt
    cnt = yield  # 获取一个数据
    while True:
        if cnt <= 0:
            print("look at here")
            cnt = yield cnt
        cnt -= 1
        time.sleep(1)
        print("ethan consume 1 hamburger. cnt=", cnt)


def cooker():
    global cnt
    gen = ethan()
    # 激活
    next(gen)
    gen.send(cnt)
    while True:
        cnt += 5
        print("cooker produce 5 hamburger. cnt=", cnt)
        gen.send(cnt) # 将会挂起, 直到下一个yield 或者j
        print("send complete")


if __name__ == "__main__":
    cooker()

    def test():
        yield 1
        time.sleep(5)
        yield 2



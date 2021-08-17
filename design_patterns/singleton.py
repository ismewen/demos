import random
import unittest
import threading

from unittest import TestCase


class MultiTonMetaClass(type):
    _lock = threading.Lock()
    multi_mapping = dict()

    # example = {
    #     "cls_name": {
    #         "ident1": [],
    #         "ident2": [],
    #     }
    # }
    def __init__(cls, cls_name, bases, attrs):
        mcs = MultiTonMetaClass
        is_eager = getattr(cls, "__is_eager__", False)
        with mcs._lock:
            if is_eager:
                mcs.init_instance(cls)

    def __call__(cls, *args, **kwargs):
        mcs = MultiTonMetaClass
        # 每次都lock unlock开销很大
        need_init = mcs.need_init_instance(cls)
        print("---need init out lock--: %s" % need_init)
        if need_init:
            with mcs._lock:
                need_init = mcs.need_init_instance(cls)
                print("---need init in lock--: %s" % need_init)
                if need_init:
                    mcs.init_instance(cls, *args, **kwargs)
        obj_num = random.randint(0, len(mcs.multi_mapping[cls][mcs.get_current_thread_flag(cls)]) - 1)
        return mcs.multi_mapping[cls][mcs.get_current_thread_flag(cls)][obj_num]

    @classmethod
    def get_current_thread_flag(mcs, cls):
        is_thread = getattr(cls, "__is_thread__", False)
        if is_thread:
            ident = threading.currentThread().ident
            return ident
        return "global"

    @classmethod
    def need_init_instance(mcs, cls):
        try:
            need_init = len(mcs.multi_mapping[cls][mcs.get_current_thread_flag(cls)]) == 0
            return need_init
        except Exception as e:
            print(e)
            return True

    @classmethod
    def init_instance(mcs, multi_cls, *args, **kwargs):
        instance_number = getattr(multi_cls, "__instance_num__", 1)
        for x in range(instance_number):
            mcs.multi_mapping.setdefault(multi_cls, dict())
            mcs.multi_mapping[multi_cls].setdefault(mcs.get_current_thread_flag(multi_cls), [])
            obj = multi_cls.__new__(multi_cls, *args, **kwargs)
            multi_cls.__init__(obj, *args, **kwargs)
            mcs.multi_mapping[multi_cls][mcs.get_current_thread_flag(multi_cls)].append(obj)


class Singleton(metaclass=MultiTonMetaClass):
    __instance_num__ = 1


class EagerMixin(object):
    __is_eager__ = True


class ThreadMixin(object):
    __is_thread__ = True


class MultiThreadSingleDog(ThreadMixin, Singleton):
    # __instance_num__ = 1
    # __is_thread__ = True

    def __init__(self):
        import time
        time.sleep(2)

class MultiTonTestcase(TestCase):

    def test_eager(self):
        class Dog(metaclass=MultiTonMetaClass):
            __is_eager__ = True
            __instance_num__ = 1
            __is_thread__ = False  # 单线程, 全局

        self.assertTrue(len(MultiTonMetaClass.multi_mapping[Dog][
                                MultiTonMetaClass.get_current_thread_flag(Dog)]) == Dog.__instance_num__)

        class Cat(metaclass=MultiTonMetaClass):
            __is_eager__ = False
            __instance_num__ = 1

        self.assertTrue(Cat not in MultiTonMetaClass.multi_mapping)
        Cat()
        self.assertTrue(len(MultiTonMetaClass.multi_mapping[Cat][
                                MultiTonMetaClass.get_current_thread_flag(Cat)]) == Cat.__instance_num__)

    def test_singleton(self):
        class Cat(metaclass=MultiTonMetaClass):
            __is_eager__ = False
            __instance_num__ = 1

        cat1 = Cat()
        cat2 = Cat()

        self.assertTrue(id(cat1) == id(cat2))

    def test_global_level(self):
        class MultiThreadDog(metaclass=MultiTonMetaClass):
            __instance_num__ = 1
            __is_thread__ = False
            __is_eager__ = False

            def __init__(self):
                import time
                time.sleep(1)

        def create_dog():
            MultiThreadDog()
        print("--------- 第一次执行 ----------")
        print("第一次会加锁")
        threadings = []
        for x in range(5):
            t = threading.Thread(target=create_dog)
            t.start()
            threadings.append(t)

        for t in threadings:
            t.join()

        objs = MultiTonMetaClass.multi_mapping[MultiThreadDog][
            MultiTonMetaClass.get_current_thread_flag(MultiThreadDog)]

        # 保证只有一个
        self.assertTrue(len({id(obj) for obj in objs}) == MultiThreadDog.__instance_num__)

        print("--------- 第二次执行 ----------")
        print("------第二次不会加锁-----")
        thread_num = 5
        for x in range(thread_num):
            t = threading.Thread(target=create_dog)
            t.start()
            threadings.append(t)

        for t in threadings:
            t.join()

    def test_thread_level(self):
        class MultiThreadSingleDog(ThreadMixin, Singleton):
            # __instance_num__ = 1
            # __is_thread__ = True
            __is_eager__ = False

            def __init__(self):
                import time
                time.sleep(2)

        threadings = []

        def create_dog():
            MultiThreadSingleDog()

        thread_num = 5
        for x in range(thread_num):
            t = threading.Thread(target=create_dog)
            t.start()
            threadings.append(t)

        for t in threadings:
            t.join()

        objs = MultiTonMetaClass.multi_mapping[MultiThreadSingleDog]
        self.assertTrue(objs)
        ids = []
        for ident, instances in objs.items():
            self.assertTrue(len(instances) == MultiThreadSingleDog.__instance_num__)
            ids.extend([id(x) for x in instances])
        assert_num = MultiThreadSingleDog.__instance_num__ * thread_num
        if MultiThreadSingleDog.__is_eager__:
            assert_num = MultiThreadSingleDog.__instance_num__ * (thread_num + 1)
        print(ids, assert_num)
        self.assertTrue(len(set(ids)) == assert_num)


if __name__ == '__main__':
    unittest.main()

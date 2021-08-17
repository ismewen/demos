import abc
from abc import ABC


class DynamicConfig(object):

    def __init__(self, build):
        self.config1 = build.config1
        self.config2 = build.config2
        self.config3 = build.config3

    def __str__(self):
        s = "%s-->%s\n" % ("config1", self.config1)
        s += "%s-->%s\n" % ("config2", self.config2)
        s += "%s-->%s\n" % ("config3", self.config3)
        return s

    class Build(object):
        config1 = None
        config2 = None
        config3 = None

        def __init__(self, config1=None, config2=None, config3=config3):
            self.config1 = config1
            self.config2 = config2
            self.config3 = config3

        def set_config1(self, config1):
            self.config1 = config1
            return self

        def set_config2(self, config2):
            self.config2 = config2
            return self

        def set_config3(self, config3):
            self.config3 = config3
            return self

        def build(self):
            if not self.config1:
                raise Exception("must set config1")
            if not self.config2:
                raise Exception("must set config2")
            return DynamicConfig(self)


class Computer(object):

    def __init__(self, build: 'Build'):
        for attr in build.__slots__:
            setattr(self, attr, getattr(build, attr))

    def __str__(self):
        s = "name: %s\n" % self.name
        s += "cpu: %s\n" % self.cpu
        s += "memory: %s\n" % self.memory
        s += "display: %s\n" % self.display
        return s

    class Build(object):

        def __init__(self, name):
            self.name = name
            self.cpu = None
            self.memory = None
            self.display = None

        __slots__ = ("cpu", "memory", "display", "name")

        def add_cpu(self, cpu):
            self.cpu = cpu
            return self

        def add_memory(self, memory):
            self.memory = memory
            return self

        def add_display(self, display):
            self.display = display
            return self

        def build(self):
            if not self.name:
                raise Exception("你见过没有名字的的电脑吗？")
            if not self.cpu:
                raise Exception("你见过没有cpu的电脑吗")
            if not self.memory:
                raise Exception("你见过没有内存的电脑吗?")
            return Computer(self)


class ABCCarBuild(abc.ABC):
    # abcBuild
    engine = None
    chassis = None
    body = None
    electrical_equipment = None

    @abc.abstractmethod
    def add_engine(self):
        pass

    @abc.abstractmethod
    def add_chassis(self):
        pass

    @abc.abstractmethod
    def add_body(self):
        pass

    @abc.abstractmethod
    def add_electrical_equipment(self):
        pass

    def get_car(self):
        return Car(self)


class Car(object):
    engine = None
    chassis = None
    body = None
    electrical_equipment = None

    def __init__(self, build: 'ABCCarBuild'):
        self.engine = build.engine
        self.chassis = build.chassis
        self.body = build.body
        self.electrical_equipment = build.electrical_equipment

    def __str__(self):
        s = "引擎: %s\n" % self.engine
        s += "底盘: %s\n" % self.chassis
        s += "车身: %s\n" % self.body
        s += "电子设备: %s\n" % self.electrical_equipment
        return s


class DabenCarBuild(ABCCarBuild):

    def add_engine(self):
        self.engine = "大奔牌发动机"

    def add_chassis(self):
        self.chassis = "大奔牌底盘"

    def add_body(self):
        self.body = "大奔牌车身"

    def add_electrical_equipment(self):
        self.electrical_equipment = "大奔牌电子设备"


class WulingHongguangBuild(ABCCarBuild):

    def add_engine(self):
        self.engine = "五菱宏光发动机"

    def add_chassis(self):
        self.chassis = "五菱宏光底盘"

    def add_body(self):
        self.body = "五菱宏光车身"

    def add_electrical_equipment(self):
        self.electrical_equipment = "五菱宏光电子设备"


class CarDirector(object):

    @classmethod
    def construct(cls, build: 'ABCCarBuild'):
        build.add_engine()
        build.add_chassis()
        build.add_body()
        build.add_electrical_equipment()
        return build.get_car()


if __name__ == "__main__":
    build = DynamicConfig.Build(
        config1=1
    ).set_config3(
        config3=3
    ).set_config2(
        config2=2
    ).build()
    print(build)
    try:
        computer = Computer.Build("ethan").add_cpu(
            cpu="8核"
        ).add_memory(
            memory="4G"
        ).add_display(
            display="27寸"
        ).build()
    except Exception as e:
        print(e)

    print(computer)
    try:
        computer = Computer.Build("ethan").add_cpu(
            cpu="8核"
        ).add_display(
            display="27寸"
        ).build()
        print(computer)
    except Exception as e:
        print(e)

    # 来一辆大奔
    print("start build an 大奔")
    daben_build = DabenCarBuild()
    daben = CarDirector.construct(daben_build)
    print(daben)

    print("start build an 五菱宏光")
    wulin_build = WulingHongguangBuild()
    wulinhongguang = CarDirector.construct(wulin_build)
    print(wulinhongguang)

class SystemOne(object):

    def op_one(self):
        pass

    def op_two(self):
        pass

    def op_three(self):
        pass


class SystemTwo(object):

    def op_one(self):
        pass

    def op_two(self):
        pass

    def op_three(self):
        pass


class Facade(object):

    def __init__(self, subsystem_one: SystemOne, subsystem_two: SystemTwo):
        self.subsystem_one = subsystem_one
        self.subsystem_two = subsystem_two

    def do_some_stuff(self):
        self.subsystem_one.op_one()
        self.subsystem_one.op_three()
        self.subsystem_two.op_two()
        self.subsystem_one.op_two()


if __name__ == "__main__":
    # 不使用外观模式
    system_one = SystemOne()
    system_two = SystemTwo()
    system_one.op_one()
    system_one.op_three()
    system_two.op_two()
    system_one.op_two()

    # 使用外观模式
    fa = Facade(system_one, system_two)
    fa.do_some_stuff()

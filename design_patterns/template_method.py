import abc


class Cook(abc.ABC):

    def heat_up_pots(self):
        print("加热锅...")

    def add_oil(self):
        print("放油...")

    def heat_up_oil(self):
        print("热油...")

    @abc.abstractmethod
    def add_dish(self):
        pass

    def topping(self):
        print("颠锅...")

    def load(self):
        print('装盘...')

    def cook(self):
        self.heat_up_pots()
        self.add_oil()
        self.heat_up_oil()
        self.add_dish()
        self.topping()
        self.load()


class CookEggplant(Cook):

    def add_dish(self):
        print("放茄子...")


class CookCarrot(Cook):
    def add_dish(self):
        print("放胡萝卜...")


if __name__ == "__main__":
    print('老板，来一份茄子')
    ce = CookEggplant()
    ce.cook()
    print("老板，来一份胡萝卜")
    cc = CookCarrot()
    cc.cook()

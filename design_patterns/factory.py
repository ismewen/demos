import abc
from abc import ABC


class Pizza(ABC):

    def prepare(self):
        pass

    def bake(self):
        pass

    def cut(self):
        pass

    def box(self):
        pass


class CheesePizza(Pizza):
    pass


class GreekPizza(Pizza):
    pass


class GoodPizza(Pizza):
    pass


def order_pizza_old(pizza_type: str) -> Pizza:
    if pizza_type == "cheese":
        pizza = CheesePizza()
    elif pizza_type == "greek":
        pizza = GreekPizza()
    elif pizza_type == "good":
        pizza = GoodPizza()
    else:
        raise Exception("Invalid pizza type")
    # 如上所述代码中存在大量的if/else根据不同的类型，创建不同的类。
    # 当添加新的类型的时候，需要修改此处，无法做到对修改关闭

    pizza.prepare()
    pizza.bake()
    pizza.cut()
    pizza.box()

    return pizza


class SimplePizzaFactory(object):

    @classmethod
    def create_pizza(cls, pizza_type) -> Pizza:
        if pizza_type == "cheese":
            pizza = CheesePizza()
        elif pizza_type == "greek":
            pizza = GreekPizza()
        elif pizza_type == "good":
            pizza = GoodPizza()
        else:
            raise Exception("Invalid pizza type")
        return pizza


class BusySimplePizzaFactory(object):

    @classmethod
    def create_pizza(cls, pizza_style: str, pizza_type) -> Pizza:
        if pizza_style == "NY":
            if pizza_type == "cheese":
                pizza = NYStyleCheesePizza()
            elif pizza_type == "greek":
                pizza = NYStyleGreekPizza()
            elif pizza_type == "good":
                pizza = NYStyleGoodPizza()
            else:
                raise Exception("Invalid pizza type")
        elif pizza_style == "Chicago":
            if pizza_type == "cheese":
                pizza = CheesePizza()
            elif pizza_type == "greek":
                pizza = GreekPizza()
            elif pizza_type == "good":
                pizza = GoodPizza()
            else:
                raise Exception("Invalid pizza type")
        else:
            raise Exception("Invalid pizza type")
        return pizza


def order_pizza(pizza_type: str) -> Pizza:
    pizza = SimplePizzaFactory.create_pizza(pizza_type)
    pizza.prepare()
    pizza.bake()
    pizza.cut()
    pizza.box()
    return pizza


class NYStyleCheesePizza(Pizza):
    pass


class NYStyleGreekPizza(Pizza):
    pass


class NYStyleGoodPizza(Pizza):
    pass


class ChicagoStyleCheesePizza(Pizza):
    pass


class ChicagoStyleGreekPizza(Pizza):
    pass


class ChicagoStyleGoodPizza(Pizza):
    pass


class ABCPizzaFactory(ABC):

    @abc.abstractmethod
    def create_pizza(self, pizza_type):
        pass


class PizzaStore(ABC):
    pizza_factory: ABCPizzaFactory

    def order_pizza(self, pizza_type: str) -> Pizza:
        pizza = self.pizza_factory.create_pizza(pizza_type=pizza_type)

        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()

        return pizza


class NYStyleABCPizzaStyleFactory(ABCPizzaFactory):

    @classmethod
    def create_pizza(cls, pizza_type) -> Pizza:
        if pizza_type == "cheese":
            pizza = NYStyleCheesePizza()
        elif pizza_type == "greek":
            pizza = NYStyleGreekPizza()
        elif pizza_type == "good":
            pizza = NYStyleGoodPizza()
        else:
            raise Exception("Invalid pizza type")
        return pizza


class ChicagoStyleABCPizzaFactory(ABCPizzaFactory):

    @classmethod
    def create_pizza(cls, pizza_type) -> Pizza:
        if pizza_type == "cheese":
            pizza = ChicagoStyleCheesePizza()
        elif pizza_type == "greek":
            pizza = ChicagoStyleGreekPizza()
        elif pizza_type == "good":
            pizza = ChicagoStyleGoodPizza()
        else:
            raise Exception("Invalid pizza type")
        return pizza


class ChicagoStylePizzaStore(PizzaStore):
    pizza_factory = ChicagoStyleABCPizzaFactory


class NYStylePizzaStore(PizzaStore):
    pizza_factory = NYStyleABCPizzaStyleFactory


class PizzaIngredientFactory(ABC):

    @classmethod
    @abc.abstractmethod
    def create_dough(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def create_sauce(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def create_cheese(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def create_veggies(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def create_clam(cls):
        pass


class NYPizzaIngredientFactory(PizzaIngredientFactory):

    @classmethod
    def create_dough(cls):
        pass

    @classmethod
    def create_sauce(cls):
        pass

    @classmethod
    def create_cheese(cls):
        pass

    @classmethod
    def create_veggies(cls):
        pass

    @classmethod
    def create_clam(cls):
        pass


class ChicagoPizzaIngredientFactory(PizzaIngredientFactory):

    @classmethod
    def create_dough(cls):
        pass

    @classmethod
    def create_sauce(cls):
        pass

    @classmethod
    def create_cheese(cls):
        pass

    @classmethod
    def create_veggies(cls):
        pass

    @classmethod
    def create_clam(cls):
        pass

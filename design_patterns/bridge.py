import abc


class ShapeBuild(object):
    draw_api = None
    shape_cls = None

    def set_cls(self, shape_cls):
        self.shape_cls = shape_cls
        return self

    def set_draw_api(self, draw_api):
        self.draw_api = draw_api
        return self

    def build(self):
        return self.shape_cls(self)


class Shape(abc.ABC):
    draw_api = None  # type: DrawAPI

    def __init__(self, build: 'ShapeBuild'):
        self.draw_api = build.draw_api

    def draw(self):
        self.draw_api.draw()


class DrawAPI(abc.ABC):

    @abc.abstractmethod
    def draw(self):
        pass


class DrawRedCircle(DrawAPI):

    def draw(self):
        print("draw red circle")


class DrawGreenCircle(DrawAPI):

    def draw(self):
        print("draw green circle")


class DrawRedRectangle(DrawAPI):
    def draw(self):
        print("draw red rectangle")


class DrawGreenRectangle(DrawAPI):
    def draw(self):
        print("draw green rectangle")


class Circle(Shape):
    pass


class Rectangle(Shape):
    pass


if __name__ == "__main__":
    red_circle = ShapeBuild().set_cls(
        Circle
    ).set_draw_api(
        DrawRedCircle()
    ).build()

    red_circle.draw()

    green_circle = ShapeBuild().set_cls(
        Circle
    ).set_draw_api(
        DrawGreenRectangle()
    ).build()

    green_circle.draw()

    red_rectangle = ShapeBuild().set_cls(
        Rectangle
    ).set_draw_api(
        DrawRedRectangle()
    ).build()

    red_rectangle.draw()

    green_rectangle = ShapeBuild().set_cls(
        Rectangle
    ).set_draw_api(
        DrawGreenRectangle()
    ).build()

    green_rectangle.draw()

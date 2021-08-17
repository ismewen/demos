import abc


class Shape(abc.ABC):

    def draw(self):
        pass


class ShapeDecorator(Shape):

    def __init__(self, shape: Shape):
        self.shape = shape

    def draw(self):
        self.shape.draw()


class Circle(Shape):

    def draw(self):
        print("Shape: circle")


class Rectangle(Shape):

    def draw(self):
        print("Shape: rectangle")


class RedBorderShapeDecorator(ShapeDecorator):

    def draw(self):
        print("Border color: Red")
        res = super(RedBorderShapeDecorator, self).draw()
        return res


class LineShapeDecorator(ShapeDecorator):

    def draw(self):
        print("Line: Wavy")
        return super(LineShapeDecorator, self).draw()


if __name__ == "__main__":
    print("---Normal---")
    circle = Circle()
    circle.draw()
    print("---RedBorder---")
    red_circle = RedBorderShapeDecorator(circle)
    red_circle.draw()
    print("---Line---")
    line_circle = LineShapeDecorator(circle)
    line_circle.draw()
    print("---line redborder---")
    lr = LineShapeDecorator(RedBorderShapeDecorator(circle))
    lr.draw()

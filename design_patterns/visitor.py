import abc


class Shape(abc.ABC):

    def accept(self, visitor):
        pass


class Visitor(abc.ABC):

    def visit_dot(self, dot):
        pass

    def visit_line(self, line):
        pass


class ExportVisitor(Visitor):

    def visit_dot(self, dot):
        print("export dot")

    def visit_line(self, line):
        print("export line")


class DrawVisitor(Visitor):

    def visit_dot(self, dot):
        print("Draw dot")

    def visit_line(self, line):
        print("Draw line")


class Dot(Shape):

    def accept(self, visitor):
        return visitor.visite_dot(self)


class Line(Shape):

    def accept(self, visitor):
        return visitor.visite_line(self)


if __name__ == "__main__":
    ev = ExportVisitor()
    ev.visit_dot(Dot())
    ev.visit_line(Line())
    dv = DrawVisitor()
    dv.visit_line(Line())
    dv.visit_dot(Dot())

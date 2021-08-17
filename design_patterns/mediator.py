import abc


class Component(abc.ABC):

    def __init__(self, mediator):
        self.mediator = mediator

    def action(self):
        pass


class Mediator(abc.ABC):

    def __init__(self):
        self.components = []  # type []Component

    def add_components(self, component: Component):
        self.components.append(component)

    def remove_components(self, component: Component):
        self.components.remove(component)


class User(Component):

    def __init__(self, name, mediator: Mediator):
        super(User, self).__init__(mediator=mediator)
        self.name = name
        mediator.add_components(self)

    def send_msg(self, msg):
        self.mediator.on_send_msg(self, msg)


class ChatRoom(Mediator):

    def on_send_msg(self, user, msg):
        for c_user in self.components:
            if c_user == user:
                continue
            print("notify: %s, msg: %s, sender: %s" % (c_user.name, msg, user.name))


if __name__ == "__main__":
    chat_room = ChatRoom()
    ethan = User(name="Ethan", mediator=chat_room)
    god = User(name="God", mediator=chat_room)
    evil = User(name="Evil", mediator=chat_room)
    angel = User(name="Angel", mediator=chat_room)
    print("Ethan send an msg")
    ethan.send_msg("hello world")

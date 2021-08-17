import abc


class TvController(object):

    def __init__(self, tv_on_command: 'Command', tv_close_command: 'Command', tv_change_channel_command: 'Command'):
        self.tv_on_command = tv_on_command
        self.tv_close_command = tv_close_command
        self.tv_change_channel_command = tv_change_channel_command

    def on(self):
        print("按下开机键...")
        self.tv_on_command.execute()

    def close(self):
        print("按下关机键...")
        self.tv_close_command.execute()

    def change_channel(self):
        print("按下换台键...")
        self.tv_change_channel_command.execute()


class Tv(object):

    def on(self):
        print("打开电视")

    def close(self):
        print("关闭电视")

    def change_channel(self):
        print("换台")


class Command(abc.ABC):

    def execute(self):
        pass


class TvOnCommand(Command):

    def __init__(self, tv: Tv):
        self.tv = tv

    def execute(self):
        self.tv.on()


class TvOffCommand(Command):

    def __init__(self, tv: Tv):
        self.tv = tv

    def execute(self):
        self.tv.close()


class TvChangeChanelCommand(Command):
    def __init__(self, tv: Tv):
        self.tv = tv

    def execute(self):
        self.tv.change_channel()


if __name__ == "__main__":
    tv = Tv()
    controller = TvController(TvOnCommand(tv), TvOffCommand(tv), TvChangeChanelCommand(tv))
    controller.on()
    controller.change_channel()
    controller.close()

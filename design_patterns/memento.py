class InputText(object):

    def __init__(self):
        self.text = ""

    def get_text(self):
        return self.text

    def set_text(self, text: str):
        self.text = text

    def append(self, input_text: str):
        self.text = self.text + input_text

    def create_snapshot(self):
        return SnapShot(input_text=self)


class SnapShot(object):

    def __init__(self, input_text: InputText):
        self.input_text = input_text
        self.text = input_text.get_text()

    def restore(self):
        self.input_text.set_text(self.text)
        return self.input_text


if __name__ == "__main__":
    input_text = InputText()
    input_text.append("do one")
    print("take an snapshot: snap_1,  current: %s" % input_text.get_text())
    snap_1 = input_text.create_snapshot()
    input_text.append("do two")
    print("take an snapshot: snap_2, current: %s" % input_text.get_text())
    snap_2 = input_text.create_snapshot()
    print("restore")
    print("restore to snap_1")
    n1 = snap_1.restore()
    print(n1.get_text())
    print("restore to snap_2")
    n2 = snap_2.restore()
    print(n2.get_text())

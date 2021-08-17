import abc
import os


class FileSystemNode(abc.ABC):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path

    @property
    @abc.abstractmethod
    def nums(self):
        # 统计文件的数量
        pass

    @property
    @abc.abstractmethod
    def size(self):
        # 统计文件的大小
        pass

    @property
    def stat(self):
        # 查看stat信息
        return os.stat(self.path)

    @property
    def file_name(self):
        return self.path.split("/")[-1]

    @abc.abstractmethod
    def print(self, depth):
        pass


class File(FileSystemNode):

    def nums(self):
        return 1

    def size(self):
        return self.stat.st_size

    def print(self, depth=0):
        print(" " * depth * 4 + self.file_name)


class Directory(FileSystemNode):

    def __init__(self, path):
        super(Directory, self).__init__(path)
        self.sub_nodes = []

    def nums(self):
        nums = 0
        for file_node in self.sub_nodes:
            nums += file_node.nums()
        return nums

    def size(self):
        size = 0
        for file_node in self.sub_nodes:
            size += file_node.size()
        return size

    def print(self, depth=0):
        print(" " * depth * 4 + "-" + self.file_name)
        for sub_node in self.sub_nodes:
            sub_node.print(depth + 1)


def create_file_tree(root_path):
    import os
    if not os.path.isdir(root_path):
        raise Exception("%s 不是一个存在的目录")
    head = Directory(root_path)
    for file_name in os.listdir(root_path):
        file_path = str(root_path) + "/" + file_name
        if os.path.isfile(file_path):
            file_node = File(file_path)
            head.sub_nodes.append(file_node)
        else:
            directory_node = create_file_tree(file_path)
            head.sub_nodes.append(directory_node)
    return head


if __name__ == "__main__":
    head = create_file_tree("/Users/ismewen/github/demos/design_patterns")
    print("打印目录树")
    head.print()
    print("size: %s" % head.size())
    print("nums: %s" % head.nums())

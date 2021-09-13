import unittest


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        print("测试开始之前，准备...")

    def tearDown(self) -> None:
        print("测试完成后，清理...")

    @unittest.skip("跳过")
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    @unittest.skipIf(1 > 0, "条件满足就跳过")
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    @unittest.skipUnless(1 > 0, "条件为真，就执行，否则就跳过")
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_some(self):
        self.assertEqual(1, 1)


class A(object):

    def who_am_i(self):
        print("A")


class B(object):

    def who_am_id(self):
        print("B")


class C(A):
    pass


class D(B):
    pass


class E(C, D):
    pass


if __name__ == '__main__':
    print(E.__mro__)

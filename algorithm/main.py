"""
一个数字， 有一个数字出现了奇数次，其他的数字出现偶数次，请找到这个数字。
一个数组， 有两个不同的数字出现了奇数次， 其他的数字出现了偶数次， 请找到这两个数字。
"""
import functools

arr = [1, 3, 3, 4, 4, 2, 2, 2, 1, 1, 5, 5]


def find(arr):
    ab = functools.reduce(lambda x, y: x ^ y, arr)
    flag = ab & (~ab + 1)
    a = ab
    for x in arr:
        if x & flag == 1:
            a ^= x
    b = ab ^ a
    return a, b

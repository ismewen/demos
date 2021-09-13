# 字符串的基本操作

#### in && not in

# 是否是子串
a, b, c = "ssss", "ss", "cc"
print(b in a)  # True
print(c in a)  # False
print(c not in a)  # True

#### 格式化
s = "we all love %s" % "php"
s = "we all love {}".format("php")
s = "we all love {php}".format(php="php")
print(s)  # we all love php

#### 常用内建函数

#### 大小写转换
s.capitalize()  # 首字母大写
s.title()  # 单词首字母大写 We All Love Php
s.lower()  # 转小写
s.upper()  # 转大写
s.swapcase() # 大小写互换

#### 统计相关
s.count("l")  # 统计l出现的次数
#### 替换
s.replace("aa", "bb")  # 将 s 中的 aa 替换成 bb
#### strip字符
s.strip()  # 去除空格
s.strip("ts")  # 首尾去除 所有的字符串 t 和 s
s.lstrip()
s.rstrip()

#### join & split
s.join(["a", "b", "c"])  # a + s + b + s + c
s.split(",")  # 以逗号进行分隔字符串，得到一个列表

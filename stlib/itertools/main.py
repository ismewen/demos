
stus = [
    {"age": 10, "name": "someOne", "id": 1},
    {"age": 10, "name": "someOne", "id": 4},
    {"age": 12, "name": "someOne", "id": 2},
    {"age": 10, "name": "someOne", "id": 4},
    {"age": 12, "name": "someOne", "id": 3},
]

from itertools import groupby
from operator import itemgetter
key_func = itemgetter("age")
res = groupby(sorted(stus, key=key_func), key=key_func)
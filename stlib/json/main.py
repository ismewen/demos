import json


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')  # 转换为字符串
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')  # 转换为字符串
        else:
            return json.JSONEncoder.default(self, value)


if __name__ == "__main__":
a = {"a": 1, "b": 2}
with open("t.json", "w+") as f:
    json.dump(a, f)
with open("t.json", "r") as f:
    b = json.load(f)
print(b, type(b))

import json
from datetime import datetime, date

dt = datetime.now()
d = date.today()

print(json.dumps({"dt": dt, "d":d}, cls=CustomJsonEncoder))
print(json.dumps({"dt": dt, "d":d}))

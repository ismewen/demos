if __name__ == "__main__":
    with open("test.txt", "w+") as f:
        f.write("fk")
        f.seek(0)
        data = f.read()
        f.readline()
        print(data)

a = {"a": 1, "b": [1, 2, 3]}
data = json.dumps(a, cls)
json.encoder
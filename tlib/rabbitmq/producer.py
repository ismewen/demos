from tlib.rabbitmq.piccolo import Piccolo


class DemoClient(Piccolo):
    listen_queue_name = "demo.server"
    listen_routing_key = "to.demo"

    publish_queue_name = "demo.client"
    publish_routing_key = "to.demo"


if __name__ == "__main__":
    d = DemoClient()
    d.publish({"hello": "word"})
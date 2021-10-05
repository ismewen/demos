from tlib.rabbitmq.piccolo import Piccolo


class DemoServer(Piccolo):
    publish_queue_name = "demo.server"
    publish_routing_key = "to.demo"

    listen_queue_name = "demo.client"
    listen_routing_key = "to.demo"


if __name__ == "__main__":
    d = DemoServer()
    d.run()
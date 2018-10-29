import Pyro4
import time


class Consumer:
    """
     This class is a generic consumer of the output of the active object tracker.
     At this moment it only displays through console out what it gets from the object tracker
    """
    def __init__(self):
        self.name = "consumer"
        self.communication_server = None
        self.output_interval = 1

    def get_info(self):
        try:
            info = self.communication_server.get_value_result_queue()
        except:
            info = "Waiting for results"

        return info

    def connect_to_channel(self):
        self.communication_server = Pyro4.Proxy("PYRONAME:CommunicationService")

    def do_task(self):
        return self.get_info()

    def output_result(self):
        print(f"Result: {self.do_task()}")

    def service_loop(self):
        while True:
            self.output_result()
            time.sleep(self.output_interval)


if __name__ == '__main__':
    print("Starting Consumer")
    consumer = Consumer()
    consumer.connect_to_channel()
    consumer.service_loop()

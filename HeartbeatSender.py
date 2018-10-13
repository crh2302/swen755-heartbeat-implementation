from multiprocessing import Process, Queue
from random import randint
import time


class HeartbeatSender:
    """" HeartbeatSender sends a heartbeat message periodically.  """

    # random_ = randint(1, 10)

    def __init__(self, queue):
        self.receiver = queue.get()
        self.sendingInterval = 3

    def send_pulse(self):
        while True:
            print("HeartbeatSender says: I am alive...")
            time.sleep(self.sendingInterval)

        # call HeartbeatReceiver.pit_a_pat()


    # Method that executes the self-driving car system task...
    def nearby_object_detection(self, value):
        print("I'm detecting nearby objects.")

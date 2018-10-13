from multiprocessing import Process, Queue
from random import randint
import time
from time import gmtime, strftime

class HeartbeatSender:
    """" HeartbeatSender sends a heartbeat message periodically.  """

    # random_ = randint(1, 10)

    def __init__(self, queue):
        self.sendingInterval = 3
        self.queue = queue

    def send_pulse(self):
        print("HeartbeatSender says: I'm alive: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        self.queue.put("send_pulse")
        time.sleep(self.sendingInterval)
        # call HeartbeatReceiver.pit_a_pat()


    # Method that executes the self-driving car system task...
    def nearby_object_detection(self, value):
        print("I'm detecting nearby objects.")

    @staticmethod
    def run(queue):
        heartbeat_sender = HeartbeatSender(queue)
        while True:
            heartbeat_sender.send_pulse()
            #Call a method from HeartbeatReceiver


            #queue.put(messages.get("RUN_TEST"))
            #time.sleep(5)





import random
import time
import threading
import multiprocessing
from time import gmtime, strftime


class HeartbeatSender:
    """" HeartbeatSender sends a heartbeat message periodically.  """

    def __init__(self, queue):
        self.sendingInterval = 3
        self.queue = queue

    def send_pulse(self):
        while multiprocessing.current_process().is_alive():
            print("HeartbeatSender says: I'm alive: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            self.queue.put("send_pulse")
            time.sleep(self.sendingInterval)

    # Method that executes the self-driving car system task...
    def nearby_object_detection(self):
        # This code block contains a fault thar will generate a ZeroDivisionError 10% of the time every 5 secs
        while True:
            r1 = random.randint(1, 100)
            r2 = random.randint(0, 9)
            result = r1 / r2
            print("Division result: " + str(result))
            time.sleep(5)

    @staticmethod
    def run(queue):
        heartbeat_sender = HeartbeatSender(queue)

        # Open a thread to send the heartbeat pulse
        t = threading.Thread(target=heartbeat_sender.send_pulse)
        t.daemon = True
        t.start()

        heartbeat_sender.nearby_object_detection()

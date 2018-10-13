import multiprocessing
import time
from time import gmtime, strftime

class HeartbeatReceiver:
    """" The HeartbeatReceiver receives the heartbeat, updates the last received time of a
    heartbeat, which is computed by  the updateTime() method.  """

    def __init__(self):
        self.checkingInterval = 3
        self.checkingTime = 0
        self.expireTime = 0
        self.lastUpdatedTime = 0

    def get_current_time(self):
        return int(time.time())

    def check_alive(self):
        current_time = self.get_current_time()
        latency_time = self.lastUpdatedTime - current_time
        print("current time: ", current_time)
        print("last updated time: ", self.lastUpdatedTime)
        return latency_time < self.checkingInterval

    def pit_a_pat(self):
        print("HeartbeatReceiver says: Invoking pit_a_pat()")
        self.update_time()

    def update_time(self):
        self.lastUpdatedTime = self.get_current_time()
        return 0

    @staticmethod
    def run(queue):
        heartbeat_receiver = HeartbeatReceiver()
        while True:
            print("HeartbeatReceiver says: I'm alive: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            msg = queue.get() # TODO This method locks the process. Should we fix this?
            if msg == "send_pulse":
                heartbeat_receiver.pit_a_pat()
            else:
                print("No message found")

            is_alive = heartbeat_receiver.check_alive()
            print("Is alive? ", is_alive)


import multiprocessing
import time

class HeartbeatReceiver:
    """" The HeartbeatReceiver receives the heartbeat, updates the last received time of a
    heartbeat, which is computed by  the updateTime() method.  """

    def __init__(self):
        self.checkingInterval = 3
        self.checkingTime = 0
        self.expireTime = 0
        self.lastUpdatedTime = 0

    def check_alive(self):
        while True:
            print("working...")
            time.sleep(self.checkingInterval)

    def pit_a_pat(self):
        # call self.update_lapse_time()
        return False

    def update_time(self):
        self.lastUpdatedTime = int(time.time())
        return 0


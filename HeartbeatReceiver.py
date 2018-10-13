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

    def test(self):
        print("HeartbeatReceiver says: If you see this message. The test was was a success")



    @staticmethod
    def run(queue):
        heartbeat_sender = HeartbeatReceiver()
        while True:
            print("HeartbeatReceiver says: I'm alive: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            msg = queue.get() # TODO This method locks the process. Should we fix this?
            if msg == "send_pulse":
                heartbeat_sender.test()
            else:
                print("No message found")

    def test(self):
        print("HeartbeatReceiver says: If you see this message. The test was was a success")


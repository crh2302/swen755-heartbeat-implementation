import multiprocessing
from threading import Thread,Timer
import time
from time import gmtime, strftime


class HeartbeatReceiver:
    """" The HeartbeatReceiver receives the heartbeat, updates the last received time of a
    heartbeat, which is computed by  the updateTime() method.  """

    def __init__(self,queue):
        self.checking_interval = 3
        self.checking_time = 0
        self.expire_time = 0
        self.last_updated_time = 0
        self.queue = queue

    def get_current_time(self):
        return int(time.time())

    def check_alive(self):
        current_time = self.get_current_time()
        latency_time = self.last_updated_time - current_time
        print("current time: ", current_time)
        print("last updated time: ", self.last_updated_time)
        return latency_time < self.checking_interval

    def pit_a_pat(self):
        print("HeartbeatReceiver says: Invoking pit_a_pat()")
        self.update_time()

    def update_time(self):
        self.last_updated_time = self.get_current_time()
        return 0

    def message_receiver(self, info):
        print(info)
        msg = self.queue.get()
        if msg == "send_pulse":
            print("HeartbeatReceiver says: Pulse received")
            self.pit_a_pat()
        else:
            print("HeartbeatReceiver says: No message found")

    def monitor_alive(self, info):
        print(info)
        is_alive = self.check_alive()
        print("Is alive? ", is_alive)

    def get_checking_interval(self):
        return self.checking_interval

    @staticmethod
    def run(queue):
        heartbeat_receiver = HeartbeatReceiver(queue)
        try:
            t1 = set_interval(1,
                              heartbeat_receiver.message_receiver,
                              "HeartbeatReceiver Thread 1 says: Waiting for pulse")
            t2 = set_interval(heartbeat_receiver.get_checking_interval(),
                              heartbeat_receiver.monitor_alive,
                              "HeartbeatReceiver Thread 2 says: Monitoring  if alive")
            t1.start()
            t2.start()
        except:
            print("Error: unable to start thread")

def set_interval(sec, func, *args):
    def func_wrapper():
        set_interval(sec, func,  *args)
        func(*args)

    t = Timer(sec, func_wrapper)
    t.start()
    return t
from threading import Thread, Timer, ThreadError
import queue
import time


class HeartbeatReceiver:
    """" The HeartbeatReceiver receives the heartbeat, updates the last received time of a
    heartbeat, which is computed by  the updateTime() method.  """

    def __init__(self, queue):
        self.checking_interval = 3
        # self.checking_time = 0
        self.pulse_verification_interval = 1
        self.expire_time = 9
        self.last_updated_time = 0
        self.queue = queue

    def get_current_time(self):
        return int(time.time())

    def check_alive(self):
        current_time = self.get_current_time()
        latency_time = current_time - self.last_updated_time
        print(
            f"HeartbeatReceiver Main Thread says: current time: {current_time}; last updated time: {self.last_updated_time}  ")
        print(
            f"HeartbeatReceiver Main Thread says: latency_time: {latency_time} < expire_time: {self.expire_time}  ")
        return latency_time < self.expire_time

    def pit_a_pat(self):
        print("HeartbeatReceiver Thread 1 says: Invoking pit_a_pat()")
        self.update_time()

    def update_time(self):
        self.last_updated_time = self.get_current_time()

    def message_receiver(self, info):
        print(info)
        msg = self.queue.get()
        if msg == "send_pulse":
            print("HeartbeatReceiver Thread 1 says: Pulse received")
            self.pit_a_pat()
        else:
            print("HeartbeatReceiver Thread 1 says: No message found")

    def monitor_alive(self, info):
        print(info)
        is_alive = self.check_alive()
        print("HeartbeatReceiver Main Thread says: Is alive? ", is_alive)
        # TODO

    def get_checking_interval(self):
        return self.checking_interval

    def get_pulse_verification_interval(self):
        return self.pulse_verification_interval

    def timed_message_receiver(self, info):
        while True:
            print(info)
            try:
                msg = self.queue.get_nowait()
            except queue.Empty as e:
                print(e)
                msg = ""

            if msg == "send_pulse":
                print("HeartbeatReceiver Thread 1 says: Pulse received")
                self.pit_a_pat()
            else:
                print("HeartbeatReceiver Thread 1 says: No message found")

            time.sleep(self.pulse_verification_interval)

    def timed_monitor_alive(self,info):
        while True:
            print(info)
            is_alive = self.check_alive()
            print("HeartbeatReceiver Main Thread says: Is alive? ", is_alive)
            time.sleep(self.checking_interval)
            # TODO



    @staticmethod
    def run(queue):
        heartbeat_receiver = HeartbeatReceiver(queue)

        t1 = set_interval(heartbeat_receiver.get_pulse_verification_interval(),
                          heartbeat_receiver.message_receiver,
                          "HeartbeatReceiver Thread 1 says: Checking for pulse")
        t2 = set_interval(heartbeat_receiver.get_checking_interval(),
                          heartbeat_receiver.monitor_alive,
                          "HeartbeatReceiver Thread 2 says: Monitoring  if alive")

    @staticmethod
    def run2(queue):
        heartbeat_receiver = HeartbeatReceiver(queue)
        try:
            t1 = Thread(target=heartbeat_receiver.timed_message_receiver, args=("HeartbeatReceiver Thread 1 says: Checking for pulse",))
            t1.start()
        except (RuntimeError, ThreadError,) as e:
            print(e)
            print(e.args)

        heartbeat_receiver.timed_monitor_alive("HeartbeatReceiver Main Thread says: Monitoring  if alive")









def set_interval(sec, func, *args):
    def func_wrapper():
        set_interval(sec, func, *args)
        func(*args)
    t = Timer(sec, func_wrapper)
    try:
        t.start()
    except (RuntimeError, ThreadError, ) as e:
        print(e)
        print(e.args)

    return t

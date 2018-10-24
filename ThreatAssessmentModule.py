from threading import Thread, Timer, ThreadError
import multiprocessing
import logging
import Pyro4
import time
from subprocess import call


@Pyro4.expose
class ThreatAssessmentModule:
    """
        This class is responsible of using the object tracking information to assess the threat level of
        nearby objects, and act accordingly.

        The class uses the Heartbeat receiver tactic to make sure that the ObjectTracker class is active
        and working.

        Attributes:
            checking_interval (int): The number that sets the interval for checking the heartbeat updates.
            pulse_verification_interval (int): The number that ...
            expire_time (int): Sets how much time should the receiver wait before declaring the heartbeat
                sender as dead.
            last_updated_time (time): Contains the timestamp of the last time the heartbeat was received.
            queue (object): The queue object used to communicate with the ThreatAssessmentModule process.
    """

    def __init__(self, queue):
        """
        The constructor for the ThreatAssessmentModule class.

        Parameters:
            queue (object): The queue object used for inter-process communication.
        """
        self.queue = queue
        self.pulse_tries_left = 3

        self.checking_interval = 3
        self.pulse_verification_interval = 1

        self.expire_time = 9
        self.last_updated_time = 0

    def get_checking_interval(self):
        """
        Gets the checking interval of the class.

        Returns:
            checking_interval (int): Integer with the class' checking interval.
        """
        return self.checking_interval

    def get_pulse_verification_interval(self):
        """
        Gets the pulse verification interval of the heartbeat tactic.

        Returns:
            pulse_verification_interval (int): Integer with the pulse verification interval of the heartbeat tactic.
        """
        return self.pulse_verification_interval

    def get_current_time(self):
        """
        Gets the current time of the system.

        Returns:
            time (time): Object with the current system's time.
        """
        return int(time.time())

    def check_alive(self):
        """
        Method that checks wherever the heartbeat pulse from the sender is alive.

        Returns:
            is_alive (bool): Says wherever the heartbeat pulse is present or not.
        """
        current_time = self.get_current_time()
        latency_time = current_time - self.last_updated_time
        return latency_time < self.expire_time

    def pit_a_pat(self):
        """
        This method calls the update_time() function of the class.

        Side Effects:
            Calls the update_time() method

        Returns:
            None.
        """
        # print("HeartbeatReceiver Thread 1 says: Invoking pit_a_pat()")
        self.update_time()

    def update_time(self):
        """
        This method updates the last_updated_time property with the current time of the system.

        Side Effects:
            Updates the last_updated_time property

        Returns:
            None.
        """
        self.last_updated_time = self.get_current_time()

    def timed_message_receiver(self, info):
        while True:
            # print(info)
            try:
                msg = self.queue.get_nowait()
            except Exception as e:
                msg = ""

            if msg == "send_pulse":
                print("HeartbeatReceiver says: Pulse received")
                self.pit_a_pat()
            else:
                print("HeartbeatReceiver says: No pulse found")

            time.sleep(self.pulse_verification_interval)

    def timed_monitor_alive(self, info):
        while True:
            # print(info)
            is_alive = self.check_alive()
            print("HeartbeatReceiver Main Thread says: Is alive? ", is_alive)

            # Start the redundant process here
            if not is_alive and self.pulse_tries_left <= 0:
                self.activate_passive_node()
                # TEST (COLD SPARING)
                # redundant_tracker = Thread(target=self.call_redundant)
                # redundant_tracker.start()
                # self.test_entro = True

            if self.pulse_tries_left > 0:
                self.pulse_tries_left = self.pulse_tries_left - 1
            time.sleep(self.checking_interval)

    def call_redundant(self):
        call(['open', '-W', '-a', 'Terminal.app', 'RedundantObjectTracker.py'])

    def activate_passive_node(self):
        self.queue = Pyro4.Proxy("PYRONAME:redundant.queue")
        print("activating backup queue", self.queue)

    @staticmethod
    def start_active_node():
        Pyro4.config.REQUIRE_EXPOSE = False
        # queue = Pyro4.Proxy("PYRONAME:heartbeat.queue")
        queue = Pyro4.Proxy("PYRONAME:active.queue")
        ThreatAssessmentModule.run(queue)

    @staticmethod
    def run(queue):
        """
        Method that runs when the class is called by Main as a process.

        Parameters:
            queue (object): The queue object used for inter-process communication.

        Returns:
            None.
        """
        heartbeat_receiver = ThreatAssessmentModule(queue)
        try:
            t1 = Thread(target=heartbeat_receiver.timed_message_receiver, args=("HeartbeatReceiver Thread 1 says: Checking for pulse",))
            t1.start()
        except (RuntimeError, ThreadError,) as e:
            print(e)
            print(e.args)

        print("activating main queue", heartbeat_receiver.queue)
        heartbeat_receiver.timed_monitor_alive("HeartbeatReceiver Main Thread says: Monitoring if alive")


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


if __name__ == '__main__':
    ThreatAssessmentModule.start_active_node()

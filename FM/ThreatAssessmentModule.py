from threading import Thread, Timer, ThreadError
import Pyro4
import time
import queue
import enum
from subprocess import call
from time import gmtime, strftime


# Enum that contains the module types for the ObjectTrackers (active or passive)
# class NodeType(enum.Enum):
#     active = 1
#     passive = 2


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

    def __init__(self, cs):
        """
        The constructor for the ThreatAssessmentModule class.

        Parameters:
            node (NodeType): Defines wherever start communication with the active or the passive process.
        """

        #self.queue = None   # the queue object used for inter-process communication. Defined in the activate_node method
        #self.activate_node(node)
        #self.current_node = node
        self.pulse_tries_left = 15

        self.checking_interval = 0.50
        self.pulse_verification_interval = 0.25

        self.expire_time = 9
        self.last_updated_time = 0
        self.fault_manager_cs = cs

    def check_alive(self):
        """
        Method that checks wherever the heartbeat pulse from the sender is alive.

        Returns:
            is_alive (bool): Says wherever the heartbeat pulse is present or not.
        """
        current_time = time.time()
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
        self.update_time()

    def update_time(self):
        """
        This method updates the last_updated_time property with the current time of the system.

        Side Effects:
            Updates the last_updated_time property

        Returns:
            None.
        """
        self.last_updated_time = time.time()

    def timed_message_receiver(self):
        while True:
            try:
                msg = self.fault_manager_cs.get_heartbeat_message()
                msg_list = msg.split("|")
                source = msg_list[0]
                event = msg_list[1]
            except IndexError as e:
                print("Invalid message format")
                event = ""
                source = ""

            except Exception as e:
                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":" + str(e))
                event = ""
                source = ""

            if event == "heartbeat_pulse":
                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":" + f"HeartbeatReceiver says: Pulse received from node: {source}")
                self.pit_a_pat()
            else:
                print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":" + "HeartbeatReceiver says: No pulse found")

            time.sleep(self.pulse_verification_interval)

    def timed_monitor_alive(self, info):
        while True:
            # print(info)
            is_alive = self.check_alive()
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":" + "HeartbeatReceiver Main Thread says: Is alive? ", is_alive)

            #Start the redundant process here
            if not is_alive and self.pulse_tries_left <= 0:
                self.activate_other_node()

            if self.pulse_tries_left > 0:
                self.pulse_tries_left = self.pulse_tries_left - 1
            time.sleep(self.checking_interval)

    def activate_other_node(self):

        try:
            self.fault_manager_cs.activate_node()
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":" + "Requesting activation of online node------------")
        except Pyro4.errors.CommunicationError as error:
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":" + f" On activate_other_node(),the communication has failed {error}")
        except Exception as error:
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":" + f" Exception: {error}")


    def run(self):
        """
        Method that runs when the class is called by Main as a process.

        Returns:
            None.
        """
        try:
            t1 = Thread(target=self.timed_message_receiver)
            t1.start()

        except (RuntimeError, ThreadError,) as e:
            print(e)
            print(e.args)

        self.timed_monitor_alive(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":"+ "HeartbeatReceiver Main Thread says: Monitoring if alive")


if __name__ == '__main__':
    # Pyro4 configuration settings
    cs = Pyro4.Proxy("PYRONAME:FMCommunicationService")
    # cs.activate_node()

    print(f"Communication service in ThreatAssessmentModule: {cs}")
    time.sleep(5)
    heartbeat_receiver = ThreatAssessmentModule(cs)
    heartbeat_receiver.run()

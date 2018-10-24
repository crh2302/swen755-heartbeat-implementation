import random
import time
import threading
import multiprocessing
import logging
import Pyro4
import queue
from time import gmtime, strftime


@Pyro4.expose
class ObjectTracker:
    """
    This class is responsible of tracking nearby objects via the car's sensor. The results are sent
    to the ThreatAssessmentModule class.

    The class uses the Heartbeat sender tactic to send periodic updates to the ThreatAssessmentModule
    class.

    Attributes:
        sending_interval (int): The number that sets the interval for the heartbeat updates.
        queue (object): The queue object used to communicate with the ThreatAssessmentModule process.
    """

    def __init__(self, queue, allow_fault):
        """
        The constructor for the ObjectTracker class.

        Parameters:
            queue (object): The queue object used for inter-process communication.
        """
        self.sending_interval = 1
        self.queue = queue
        self.allow_fault = allow_fault

    def send_pulse(self):
        """
        The function responsible of sending the heartbeat pulse to the ThreatAssessmentModule process.
        This function is started by an internal daemon thread and runs concurrently with the rest of
        the process.

        Parameters:
            None.

        Side Effects:
            Modifies the queue property.

        Returns:
            None.
        """
        while multiprocessing.current_process().is_alive():
            print("HeartbeatSender says: I'm alive: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            self.queue.put("send_pulse")
            time.sleep(self.sending_interval)

    # Method that executes the self-driving car system task...
    def detect_nearby_object(self):
        """
        The domain function responsible for detecting nearby objects.
        This function contains the code block responsible of generating the fault for the purposes of this
        assignment.

        Parameters:
            None.

        Side Effects:
            Executes the send_proximity_coordinates() method.

        Returns:
            None.
        """
        while True:
            result = self.calculate_proximity()
            self.send_proximity_coordinates(result)
            time.sleep(5)

    def calculate_proximity(self):
        # This code block contains a fault thar will generate a ZeroDivisionError 10% of the time every 5 secs
        r1 = random.randint(1, 100)
        if self.allow_fault:
            r2 = random.randint(0, 9)  # <-- inserted fault
        else:
            r2 = random.randint(1, 9)

        result = r1 / r2
        print("PROXIMITY --> Object is: " + str(result) + " meters away.")
        return result

    def send_proximity_coordinates(self, data):
        """
        Function that sends the data from the detected objects and sends it to the ThreatAssessmentModule
        (domain-specific, not implemented).

        Parameters:
            data (float): The result from the operation from the detect_nearby_object() method

        Returns:
            data (float): The processed result from the operation from the detect_nearby_object() method
        """
        # Do something here
        data = data + 1
        return data

    @staticmethod
    def run(queue, allow_fault):
        """
        Method that runs when the class is called by Main as a process.

        Parameters:
            queue (object): The queue object used for inter-process communication.

        Returns:
            None.
        """
        heartbeat_sender = ObjectTracker(queue, allow_fault)

        # Open a thread to send the heartbeat pulse
        t = threading.Thread(target=heartbeat_sender.send_pulse)
        t.daemon = True
        t.start()

        heartbeat_sender.detect_nearby_object()

    @staticmethod
    def start_object_tracker():
        multiprocessing.log_to_stderr(logging.INFO)
        Pyro4.config.REQUIRE_EXPOSE = False

        daemon = Pyro4.Daemon()  # make a Pyro4 daemon
        ns = Pyro4.locateNS()  # find the name server
        queue = multiprocessing.Queue()

        # Create the Queue object and register it on the Pyro4 proxy
        queue_uri = daemon.register(queue)
        ns.register("heartbeat.queue", queue_uri)
        sender_process = multiprocessing.Process(name='Active Process', target=ObjectTracker.run, args=(queue,))
        sender_process.start()

        daemon.requestLoop()


if __name__ == '__main__':
    ObjectTracker.start_object_tracker()

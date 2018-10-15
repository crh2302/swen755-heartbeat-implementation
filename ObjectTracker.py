import random
import time
import threading
import multiprocessing
from time import gmtime, strftime


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

    def __init__(self, queue):
        """
        The constructor for the ObjectTracker class.

        Parameters:
            queue (object): The queue object used for inter-process communication.
        """
        self.sending_interval = 3
        self.queue = queue

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
        # This code block contains a fault thar will generate a ZeroDivisionError 10% of the time every 5 secs
        while True:
            r1 = random.randint(1, 100)
            r2 = random.randint(0, 9)
            result = r1 / r2
            print("Division result: " + str(result))
            self.send_proximity_coordinates(result)
            time.sleep(5)

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
    def run(queue):
        """
        Method that runs when the class is called by Main as a process.

        Parameters:
            queue (object): The queue object used for inter-process communication.

        Returns:
            None.
        """
        heartbeat_sender = ObjectTracker(queue)

        # Open a thread to send the heartbeat pulse
        t = threading.Thread(target=heartbeat_sender.send_pulse)
        t.daemon = True
        t.start()

        heartbeat_sender.detect_nearby_object()

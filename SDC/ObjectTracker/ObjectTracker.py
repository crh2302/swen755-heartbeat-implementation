import random
import time
import threading
import multiprocessing
import logging
import Pyro4
from time import gmtime, strftime
from SDC.ObjectTracker.constants import LOG_PIPELINE_FILENAME


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

    def __init__(self, cs, allow_fault):
        """
        The constructor for the ObjectTracker class.

        Parameters:
            cs (object): The object containing the queue used for inter-process communication.
        """
        self.sending_interval = 1
        self.fault_manager_cs = cs
        self.allow_fault = allow_fault
        self.time_between_steps = 5
        self.isActive = False
        self.id = 2


        # Array containing the method steps to the Pipe-And-Filter pattern
        self.pipeline_steps = [
            self.split_string,
            self.convert_to_int,
            self.get_sum_and_size,
            self.get_average
        ]

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
                try:
                    if self.isActive:
                        message = str(self.id) + "|"+ "heartbeat_pulse"
                        self.fault_manager_cs.put_heartbeat_message(message)
                        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":Sending heartbeat message: I'm alive")
                    else:
                        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":Not sending heartbeat message")

                except Pyro4.errors.NamingError as naming_error:
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":Sending heartbeat message:{naming_error}. Check if pyro4 server is online. Run pyro4-ns")
                except Exception as e:
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + f":Sending heartbeat message:{e}.")

                time.sleep(self.sending_interval)

    # Method that executes the self-driving car system task...
    # def detect_nearby_object(self):
    #     """
    #     The domain function responsible for detecting nearby objects.
    #     This function contains the code block responsible of generating the fault for the purposes of this
    #     assignment.
    #
    #     Parameters:
    #         None.
    #
    #     Side Effects:
    #         Executes the send_proximity_coordinates() method.
    #
    #     Returns:
    #         None.
    #     """
    #     while True:
    #         self.calculate_proximity()
    #         time.sleep(5)

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

    def post_results(self, data):
        """
        Function that sends the data from the detected objects and sends it to the ThreatAssessmentModule
        (domain-specific, not implemented).

        Parameters:
            data (float): The result from the operation from the detect_nearby_object() method

        Returns:
            data (float): The processed result from the operation from the detect_nearby_object() method
        """
        # Do something here

        #self.calculate_proximity()
        if self.isActive:
            cs = Pyro4.Proxy("PYRONAME:CommunicationService")
            print(f"Communication service in object tracker {cs}")
            try:
                cs.set_value_result_queue(data)
            except:
                pass

    def calculate_pipeline_data(self, data, last_step=""):
        def get_step_index(items, step_name):
            for index, step in enumerate(items):
                if step.__name__ == step_name:
                    return index
                else:
                    continue
            return -1

        if last_step != "":
            step_index = get_step_index(self.pipeline_steps, last_step)
            remaining_steps = self.pipeline_steps[step_index + 1:]
            print(remaining_steps)
            result = self.combine_pipeline(data, remaining_steps)
        else:
            result = self.combine_pipeline(data, self.pipeline_steps)
        return result

    # Processing step methods
    @staticmethod
    def split_string(item):
        # First step: split a String of the form "1,2,3,4,5" on an array, using commas as the delimiter
        # Input: "1,2,3,4,5" => Output: ["1","2","3","4","5"]
        result = item.split(',')
        with open(LOG_PIPELINE_FILENAME, "a") as file:
            file.write("split_string;" + repr(result) + "\n")
        return result

    @staticmethod
    def convert_to_int(item):
        # Second step: converts the Strings of the previous array into integers
        # Input: ["1","2","3","4","5"] => Output: [1,2,3,4,5]
        result = [int(i) for i in item]
        with open(LOG_PIPELINE_FILENAME, "a") as file:
            file.write("convert_to_int;" + repr(result) + "\n")
        return result

    @staticmethod
    def get_sum_and_size(items):
        # Processing for this step goes here
        # Third step: takes the array of integers, and returns a 'sum' and a 'size' value in a dictionary
        # Input: [1,2,3,4,5] => Output: { 'sum': 15, 'size': 5 }
        result = {'sum': sum(items), 'size': len(items)}
        with open(LOG_PIPELINE_FILENAME, "a") as file:
            file.write("get_sum_and_size;" + repr(result) + "\n")
        return result

    @staticmethod
    def get_average(item):
        # Fourth step: use the sum and size values to calculate the average (sum / size)
        # Input: { 'sum': 15, 'size': 5 } => Output: 3
        result = item['sum'] / item['size']
        with open(LOG_PIPELINE_FILENAME, "a") as file:
            file.write("get_average;" + repr(result) + "\n")
        return result
    # End of processing step methods

    def combine_pipeline(self, source, pipeline):
        """
        Combines source and pipeline and return a generator.
        """
        gen = source
        for step in pipeline:
            gen = step(gen)
            print("The result of the step " + step.__name__ + " is: ")
            print(gen)
            time.sleep(self.time_between_steps)
        return gen


    @staticmethod
    def run(allow_fault):

        """
        Method that runs when the class is called by Main as a process.

        Parameters:
            queue (object): The queue object used for inter-process communication.

        Returns:
            None.
        """
        cs = Pyro4.Proxy("PYRONAME:FMCommunicationService")
        object_tracker = ObjectTracker(cs, allow_fault)

        try:
            daemon = Pyro4.Daemon()
            print("Locating Pyro4 nameserver")
            ns = Pyro4.locateNS()
            print("Pyro4 nameserver located")
            print("Registering ObjectTracker"+str(object_tracker.getID()))
            cs = Pyro4.Proxy("PYRONAME:FMCommunicationService")
            object_tracker = ObjectTracker(cs, allow_fault)
            uri = daemon.register(object_tracker)
            registering_string = "ObjectTracker"+str(object_tracker.getID())
            ns.register(registering_string, uri)
            print("subscribing:")
            cs.subscribe(registering_string)
            print("Registration completed")
            print("Ready.")
            t2 = threading.Thread(target=daemon.requestLoop)
            t2.daemon = True
            t2.start()

        except Pyro4.errors.NamingError as naming_error:
            print(f"{naming_error}. Check if Pyro4 service is online. Run pyro4-ns")
        except Exception as e:
            print(f"Exception at main(). More info:{e}")

        t = threading.Thread(target=object_tracker.send_pulse)
        t.daemon = True
        t.start()

        #t.join()


        print("LLEGO  AQUI")

        #object_tracker.detect_nearby_object()

        # Synchronization code:
        # TODO: This should run on the RedundantObjectTracker, and only when the Active process is down
        while True:
            # Get the input data
            # TODO: This is hardcoded for now, but the data should come from a Pyro4 queue
            data = "1,2,3,4,5"

            # TODO: Synchronize with the pipeline-log.txt to check the last executed method
            last_line = open(LOG_PIPELINE_FILENAME, "r").readlines()[-1]
            function_name = last_line.split(';')[0]
            function_result = eval(last_line.split(';')[1])  # eval is used to convert from string to object

            # TODO:
            # The 'data' parameter here should be either the input (for the active tracker)
            # or the function_result (for the redundant tracker)
            # The 'last_step' parameter should have the function_name on the redundant tracker
            result = object_tracker.calculate_pipeline_data(data, "")
            object_tracker.post_results(result)

            print("The end result of the pipeline is: " + str(result))

    # @staticmethod
    # def start_object_tracker():
    #     multiprocessing.log_to_stderr(logging.INFO)
    #     Pyro4.config.REQUIRE_EXPOSE = False
    #
    #     daemon = Pyro4.Daemon()  # make a Pyro4 daemon
    #     ns = Pyro4.locateNS()  # find the name server
    #
    #     # Create the Queue object and register it on the Pyro4 proxy
    #     queue_hb = multiprocessing.Queue()
    #     queue_uri = daemon.register(queue_hb)
    #     ns.register("heartbeat.queue", queue_uri)
    #
    #     sender_process=multiprocessing.Process(name='Active Process', target=ObjectTracker.run, args=(queue_hb,))
    #     sender_process.start()
    #
    #     daemon.requestLoop()
    # def post_result(self):
    #     pass

    def getID(self):
        return self.id

    @Pyro4.expose
    def activate(self):
        print("activate")
        if(self.isActive):
            self.isActive = False
        else:
            self.isActive = True





    def update(self,event):
        if "active_node_selection" == event:
            pass


if __name__ == '__main__':
    ObjectTracker.run(False)

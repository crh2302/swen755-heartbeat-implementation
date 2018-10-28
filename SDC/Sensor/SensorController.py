from time import sleep
from Pyro4 import Proxy
SENSOR_DATA_FILENAME = "sensor_data.txt"


class SensorController:
    def __init__(self, _id, name):
        self.name = name
        self.id = _id
        self.read_count = 0
        self.sensor_connection = None

    def connect_to_sensor(self):
        self.sensor_connection = open(SENSOR_DATA_FILENAME, "r")

    def next_read(self):
        try:
            line = self.sensor_connection.readline()
        except ValueError:
            print("No Connection")

    def read_data(self):
        try:
            line = self.sensor_connection.readline()
            self.read_count += 1
        except ValueError:
            print("No Connection")
        return line

    def read_and_process(self):
        return self.read_data().rstrip("\n\r").replace(",", "|")


if __name__ == '__main__':

    sc = SensorController("1", "pos_proximity")
    sc.connect_to_sensor()
    sc.next_read()
    cs = Proxy("PYRONAME:CommunicationService")

    while True:
        sensor_input_data = sc.read_and_process()
        print(sensor_input_data)
        cs.set_value_sensor_queue(sensor_input_data)
        sleep(1)
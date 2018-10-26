import Pyro4
import multiprocessing
import queue
from time import gmtime, strftime
from multiprocessing import Process, Manager



class FMCommunicationService:

    def __init__(self):
        queue_maxsize = 1
        self.heartbeat_queue = multiprocessing.Queue(queue_maxsize)
        manager = Manager()
        self.subscribers = manager.list()

    @Pyro4.expose
    def get_subscribers(self):
         print("subscribers")
         return self.subscribers

    @Pyro4.expose
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    @Pyro4.expose
    def unsubscribe(self,subscriber):
        self.subscribers.remove(subscriber)

    @Pyro4.expose
    def activate_node(self):
        for item in self.subscribers:
            m = Pyro4.Proxy("PYRONAME:"+item)
            try:
                m.activate()
                print("activate_node try")
            except Exception:
                raise Exception("empty object")
                print("activate_node excep")


    @Pyro4.expose
    def get_heartbeat_message(self):
        try:
            hb_msg = self.heartbeat_queue.get(block=False)
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + f":Heartbeat message requested and sent: [{hb_msg}]")
        except queue.Empty:
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ":Heartbeat message requested but Heartbeat message queue empty")
            raise Exception("Heartbeat message queue is empty no message received")

        return hb_msg

    @Pyro4.expose
    def put_heartbeat_message(self, ele):
        try:
            self.heartbeat_queue.put(ele,block=False)
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + f":Heartbeat message received: [{ele}]")
        except queue.Full:
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + f":Heartbeat message received but queue is full message lost: [{ele}]")
            raise Exception('Heartbeat message queue is full')


def init():
    try:
        daemon = Pyro4.Daemon()
        print("Locating Pyro4 nameserver")
        ns = Pyro4.locateNS()
        print("Pyro4 nameserver located")
        print("Registering FMCommunicationService")
        cs = FMCommunicationService()
        uri = daemon.register(cs)
        ns.register("FMCommunicationService", uri)
        print("Registration completed")
        print("Ready.")
        daemon.requestLoop()
    except Pyro4.errors.NamingError as naming_error:
        print(f"{naming_error}. Check if Pyro4 service is online. Run pyro4-ns")
        init()
    except Exception as e:
        print(f"Exception at main(). More info:{e}")




if __name__ == '__main__':
    print("Starting FMCommunicationServer")
    init()



import Pyro4
import multiprocessing


class CommunicationService:

    def __init__(self):
        self.result_queue = multiprocessing.Queue()

    @Pyro4.expose
    def get_value_result_queue(self):
        return self.result_queue.get(block=False)

    @Pyro4.expose
    def set_value_result_queue(self,ele):
        return self.result_queue.put(ele)


def init():
    try:
        daemon = Pyro4.Daemon()
        print("Locating Pyro4 nameserver")
        ns = Pyro4.locateNS()
        print("Pyro4 nameserver located")
        print("Registering CommunicationService")
        cs = CommunicationService()
        cs.set_value_result_queue("Test_result_queue")
        uri = daemon.register(cs)
        ns.register("CommunicationService", uri)
        print("Registration completed")
        print("Ready.")
        daemon.requestLoop()
    except Pyro4.errors.NamingError as naming_error:
        print(f"{naming_error}. Check if Pyro4 service is online. Run pyro4-ns")
        init()
    except Exception as e:
        print(f"Exception at main(). More info:{e}")

if __name__ == '__main__':
    print("Starting CommunicationServer")
    init()


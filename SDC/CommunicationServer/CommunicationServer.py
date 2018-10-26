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


if __name__ == '__main__':
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    cs = CommunicationService()
    cs.set_value_result_queue("Test_result_queue")
    uri = daemon.register(cs)
    ns.register("CommunicationService", uri)
    daemon.requestLoop()


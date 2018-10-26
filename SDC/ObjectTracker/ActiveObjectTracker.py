#!//usr/local/Cellar/python3/3.6.3/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import multiprocessing
import Pyro4
from SDC.ObjectTracker import ObjectTracker


if __name__ == '__main__':
    Pyro4.config.REQUIRE_EXPOSE = False

    daemon = Pyro4.Daemon()  # make a Pyro4 daemon
    ns = Pyro4.locateNS()  # find the name server
    queue = multiprocessing.Queue()

    # Create the Queue object and register it on the Pyro4 proxy
    queue_uri = daemon.register(queue)
    print("Running <Active> Node :", str(queue_uri))

    ns.register("active.queue", queue_uri)
    sender_process = multiprocessing.Process(name='Active Process', target=ObjectTracker.run, args=(queue, True))
    sender_process.start()

    daemon.requestLoop()

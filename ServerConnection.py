import multiprocessing
import Pyro4


Pyro4.config.REQUIRE_EXPOSE = False

daemon = Pyro4.Daemon()  # make a Pyro4 daemon
ns = Pyro4.locateNS()  # find the name server
queue = multiprocessing.Queue()

# Create the Queue object and register it on the Pyro4 proxy
queue_uri = daemon.register(queue)
ns.register("heartbeat.queue", queue_uri)

from multiprocessing import Process, Queue
from HeartbeatSender import HeartbeatSender
from HeartbeatReceiver import HeartbeatReceiver
import multiprocessing
import logging

if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.INFO)

    # Step 1 :
    queue = Queue()

    # Step 2
    sender_process = Process(name='HeartbeatSender Process', target=HeartbeatSender.run, args=(queue,))
    receiver_process = Process(name='HeartbeatReceiver Process', target=HeartbeatReceiver.run2, args=(queue,))

    # Step 3
    sender_process.start()
    receiver_process.start()

    sender_process.join()
    receiver_process.join()

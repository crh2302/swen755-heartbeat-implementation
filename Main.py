from multiprocessing import Process, Queue
from ObjectTracker import ObjectTracker
from ThreatAssessmentModule import ThreatAssessmentModule
import multiprocessing
import logging

if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.INFO)

    # Step 1 :
    queue = Queue()

    # Step 2
    sender_process = Process(name='HeartbeatSender Process', target=ObjectTracker.run, args=(queue,))
    receiver_process = Process(name='HeartbeatReceiver Process', target=ThreatAssessmentModule.run, args=(queue,))

    # Step 3
    sender_process.start()
    receiver_process.start()

    sender_process.join()
    receiver_process.join()

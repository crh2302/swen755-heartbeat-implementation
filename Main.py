from multiprocessing import Process, Queue
import HeartbeatSender
from HeartbeatReceiver import HeartbeatReceiver


if __name__ == '__main__':
    queue = Queue()
    sender = HeartbeatSender()
    receiver = HeartbeatReceiver()

    sender.send_pulse()

    sender_process = Process(target=HeartbeatSender, args=(queue,))
    sender_process.start()



    # receiver = HeartbeatReceiver()
    # receiver.check_alive()
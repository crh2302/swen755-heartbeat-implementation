from multiprocessing import Process, Queue, Pipe
from HeartbeatSender import HeartbeatSender
from HeartbeatReceiver import HeartbeatReceiver

if __name__ == '__main__':
    '''
    queue = Queue()
    sender = HeartbeatSender()
    receiver = HeartbeatReceiver()

    sender.send_pulse()

    sender_process = Process(target=HeartbeatSender, args=(queue,))
    sender_process.start()
    '''

    # receiver = HeartbeatReceiver()
    # receiver.check_alive()

    # Cervantes Steps
    # Step 1 : Creating a way so that the processes can interact (Creating the queue or pipe)
    # Step 2 : Creating Processes
    # Step 3 : Starting processes


    # Step 1 :
    queue = Queue()
    #sender_conn, receiver_conn = Pipe()

    # Step 2


    sender_process = Process(target=HeartbeatSender.run, args=(queue,))
    receiver_process = Process(target=HeartbeatReceiver.run,args=(queue,))

    # Step 3
    sender_process.start();
    receiver_process.start();
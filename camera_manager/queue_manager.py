from multiprocessing.managers import BaseManager
from multiprocessing import Queue
from camera_manager.lastest_frame import LatestFrame0, LatestFrame1


class QueueManager(BaseManager):
    """
        This is a class acts like a server, such that different
        clients can register a un-used name to get a queue and
        transmit data using the queue.
    """

    # a port which the server is listening to
    PORT = 14311

    # a dictionary for queues, with the name as keys and the value as the queue
    queues = {}


    @classmethod
    def apply(cls, name):
        if name in QueueManager.queues:
            print('name: %s already exists' % name)
            return
        else:
            print('create new entity: %s' % name)
            QueueManager.queues[name] = Queue()
            QueueManager.register(name, callable=lambda: QueueManager.queues[name])


    @classmethod
    def create_manager(cls):
        QueueManager.register('LatestFrame0', callable=lambda:LatestFrame0)
        QueueManager.register('LatestFrame1', callable=lambda: LatestFrame1)
        m = QueueManager(address=('', QueueManager.PORT), authkey=b'deepmagicsecret')
        return m



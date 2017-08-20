from camera_manager.queue_manager import QueueManager
from camera_manager.config import cameras


def get_manager(name):
    QueueManager.apply(name)
    podm = QueueManager.create_manager()
    podm.connect()
    return podm


if __name__ == '__main__':
    for camera in cameras:
        QueueManager.apply(camera)

    pod_manager = QueueManager.create_manager()
    server = pod_manager.get_server()
    server.serve_forever()
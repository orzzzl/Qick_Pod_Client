from camera_manager.queue_manager import QueueManager
from time import sleep
import cv2


m = QueueManager.create_manager()
m.connect()
lf = m.LatestFrame1()


while True:
    frame = lf.get_latest()
    print(frame)
    cv2.imshow('r', frame['frame'])
    cv2.waitKey(delay=1)
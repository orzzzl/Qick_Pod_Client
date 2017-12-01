from camera_manager.queue_manager import QueueManager
from time import sleep
from datetime import datetime
import cv2


m = QueueManager.create_manager()
m.connect()
lf = m.LatestFrame0()

cnt = 0
start_time = datetime.now()

fourcc_code = cv2.VideoWriter_fourcc(*'H264')
vw = cv2.VideoWriter('test_depth_r.avi', fourcc_code, 25.0, (360, 640))

while True:
    depth = lf.get_depth()
    cnt += 1
    secs = datetime.now()
    frame = cv2.merge((depth, depth, depth))
    print(frame.shape)
    vw.write(frame)
    #cv2.imshow('r', frame['frame'])
    #cv2.waitKey(delay=1)
    cv2.waitKey(1)
    if cnt >= 100:
        break

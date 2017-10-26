from camera_manager.queue_manager import QueueManager
from kinnect_service.kinnect import KinectCamera
import numpy as np
import cv2
import sys


kinect_right=  KinectCamera(1)
kinect_left = KinectCamera(0)
m = QueueManager.create_manager()
m.connect()
lf = m.LatestFrame0()
rf = m.LatestFrame1()


while True:
    frame0, depth0 = kinect_left.get_frames()
    frame1, depth1 = kinect_right.get_frames()
    lf.set(frame0, depth0)
    rf.set(frame1, depth1)
    # if lf.get_session_id() is not -1:
    #     lf.set_ai(frame0, depth0)
    # if rf.get_session_id() is not -1:
    #     rf.set_ai(frame1, depth1)
    cv2.waitKey(5)

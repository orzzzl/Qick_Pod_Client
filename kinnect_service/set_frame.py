from camera_manager.queue_manager import QueueManager
from kinnect_service.kinnect import KinectCamera
from multiprocessing import Process
import numpy as np
import cv2
import sys
import pickle


kinect_right=  KinectCamera(1)
kinect_left = KinectCamera(0)
m = QueueManager.create_manager()
m.connect()
lf = m.LatestFrame0()
rf = m.LatestFrame1()


def process_frame(f, isdep):
    if isdep:
        f = f[1:1081,:]
        #f = (f / 4500.0 * 255).astype(np.uint8)
        f[np.where(f>3050)] = 3050
        f[np.where(f<500)] = 500
        f = ((f - 500) / 10).astype(np.uint8)

        #f = cv2.merge((f, f, f))
    #print(f.shape)
    frame = cv2.resize(f, (1080 // 3, 1920 // 3))
    return frame

# def dump_depth(file_name, data):
#     with open(file_name, 'wb') as f:
#         pickle.dump(data, f)
#
# fourcc_code = cv2.VideoWriter_fourcc(*'H264')
# vw_l = cv2.VideoWriter('test_l_0.avi', fourcc_code, 20.0, (1920, 1080))
# vw_r = cv2.VideoWriter('test_r_0.avi', fourcc_code, 20.0, (1920, 1080))
# depth_l = []
# depth_r = []
# cnt = 0
# idx = 0

while True:
    frame0, depth0 = kinect_left.get_frames()
    frame1, depth1 = kinect_right.get_frames()
    frame0_p = process_frame(frame0, False)
    frame1_p = process_frame(frame1, False)
    depth0_p = process_frame(depth0, True)
    depth1_p = process_frame(depth1, True)
    # vw_l.write(frame0)
    # vw_r.write(frame1)
    # depth_l.append(depth0)
    # depth_r.append(depth1)
    # cnt += 1
    lf.set(frame0_p, depth0_p)
    rf.set(frame1_p, depth1_p)
    # if lf.get_session_id() is not -1:
    #     lf.set_ai(frame0, depth0)
    # if rf.get_session_id() is not -1:
    #     rf.set_ai(frame1, depth1)
#     print(cnt)
#     if cnt >= 1000:
#         break
#
# dump_depth('dep0', depth_l)
# dump_depth('dep1', depth_r)
# vw_l.release()
# vw_r.release()


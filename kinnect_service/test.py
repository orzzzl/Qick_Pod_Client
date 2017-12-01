from camera_manager.queue_manager import QueueManager
from kinnect_service.kinnect import KinectCamera
import numpy as np
import cv2
import sys
import pickle
import bz2

kinect_right =  KinectCamera(0)
kinect_left = KinectCamera(1)

fourcc_code = cv2.VideoWriter_fourcc(*'H264')
vw = cv2.VideoWriter('test_depth_r.avi', fourcc_code, 25.0, (1920, 1080))
vw_rgb = cv2.VideoWriter('test_rgb_r.avi', fourcc_code, 25.0, (1920, 1080))
vw_l = cv2.VideoWriter('test_depth_l.avi', fourcc_code, 25.0, (1920, 1080))
vw_rgb_l = cv2.VideoWriter('test_rgb_l.avi', fourcc_code, 25.0, (1920, 1080))
cnt = 0
idx = 0


def save(filename, myobj):
    """
    save object to file using pickle

    @param filename: name of destination file
    @type filename: str
    @param myobj: object to save (has to be pickleable)
    @type myobj: obj
    """

    try:
        f = bz2.BZ2File(filename, 'wb')
    except:
        sys.stderr.write('File ' + filename + ' cannot be written\n')
        return

    pickle.dump(myobj, f, protocol=2)
    f.close()


while True:
    frame, depth = kinect_right.get_frames()
    frame_l, depth_l = kinect_left.get_frames()
    vw_rgb.write(frame)
    vw_rgb_l.write(frame_l)

    depth = (depth[1:1081,:]/4500.0*255).astype(np.uint8)
    depth_l = (depth_l[1:1081, :]/4500.0*255).astype(np.uint8)
    frame = cv2.merge((depth, depth, depth))
    vw_l.write(cv2.merge((depth_l, depth_l, depth_l)))
    vw.write(frame)
    cnt += 1
    print(cnt)
    cv2.waitKey(1)
    if cnt == 100:
        break

vw.release()
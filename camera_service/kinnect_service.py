import cv2
import os
from datetime import datetime
from threading import Thread
import requests
import numpy as np
from camera_manager.queue_manager import QueueManager
from time import sleep
from camera_service.kinnect import KinectCamera
import sys


class Camera:
    fourcc_code = cv2.VideoWriter_fourcc(*'H264')
    frame_rate = 20.0
    frame_count_interval = 100
    video_dimension = (int(1080/3), int(1920/3))
    data_path_prefix = '/home/salil/PycharmProjects/PodClient/data/'

    def __init__(self, camera_idx):
        self.is_on = True
        self.is_recording = False
        self.camera_idx = camera_idx
        self.data_path = Camera.data_path_prefix + str(camera_idx) + '/'
        if os.path.exists(self.data_path) is False:
            os.mkdir(self.data_path)
        self.kinnect = None
        self.m = QueueManager.create_manager()
        self.m.connect()
        sleep(2)
        if self.camera_idx == 0:
            self.kinnect = self.m.LatestFrame0()
        else:
            self.kinnect = self.m.LatestFrame1()


    def write_to_db(self, file_name):
        url = 'http://127.0.0.1:14310/coordinator/write_file_to_db?file_name=%s&camera_idx=%s'
        Thread(target=requests.get, args=(url % (file_name, self.camera_idx), )).start()


    def rotate_bound(self, image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))

    def set_on(self):
        self.is_on = True

    def set_off(self):
        self.is_on = False

    def set_ai_on(self):
        pass

    def set_ai_off(self):
        pass

    def process_frame(self, f, idx):
        if idx == 1:
            frame = self.rotate_bound(f, 270)
        else:
            frame = self.rotate_bound(f, 90)
        frame = cv2.resize(frame, self.video_dimension)
        return frame

    def record(self):
        self.frame_count = 0
        self.is_recording = True
        while(self.is_recording):
            file_name = str(datetime.now()).replace(' ', '_') + '.avi'
            print('recording file: %s' % file_name)
            vw = cv2.VideoWriter(self.data_path + file_name, Camera.fourcc_code, Camera.frame_rate, Camera.video_dimension)
            for frame_idx in range(Camera.frame_count_interval):
                if not self.is_on or not self.is_recording:
                    vw.release()
                    self.write_to_db(file_name)
                    return
                else:
                    frame = self.kinnect.get()
                    frame = self.process_frame(frame, self.camera_idx)
                   # frame = self.kinect.get_frames()[0]
                    # frame = cv2.resize(frame, self.video_dimension)
                    # else:
                    #    frame = self.rotate_bound(frame, 270)
                    vw.write(frame)
                    cv2.waitKey(15)
                    self.frame_count += 1
            vw.release()
            self.write_to_db(file_name)


    def stop_recording(self):
        print('Camera %s, total_frames: %s' % (self.camera_idx, self.frame_count))
        self.frame_count = 0
        self.is_recording = False



    def __del__(self):
        self.kinnect.__del__()



if __name__ == '__main__':
    c = Camera(0)
    c.record()

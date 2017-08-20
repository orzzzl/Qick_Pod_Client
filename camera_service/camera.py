import cv2
from datetime import datetime
from threading import Thread
from camera_manager.main import get_manager
import requests
import os


class Camera:
    fourcc_code = cv2.VideoWriter_fourcc(*'H264')
    frame_rate = 15.0
    frame_count_interval = 100
    video_dimension = (320, 240)
    data_path_prefix = '/home/salil/PycharmProjects/PodClient/data/'

    def __init__(self, camera_idx):
        self.camera = None
        self.camera_idx = camera_idx
        self.camera_name = 'camera%s' % camera_idx
        self.is_on = False
        self.data_path = Camera.data_path_prefix + str(camera_idx) + '/'
        if os.path.exists(self.data_path) is False:
            os.mkdir(self.data_path)
        self.send_data_to_ai = False
        self.is_recording = False
        self.manager = None
        self.ai_queue = None
        self.session_id = 250
        self.frame_count = 0


    def write_to_db(self, file_name):
        url = 'http://127.0.0.1:14310/coordinator/write_file_to_db?file_name=%s&camera_idx=%s'
        Thread(target=requests.get, args=(url % (file_name, self.camera_idx), )).start()

    def set_on(self):
        print('camera setting on')
        if self.camera is not None:
            return
        self.camera = cv2.VideoCapture(self.camera_idx)
        assert(self.camera.isOpened())
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, Camera.video_dimension[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Camera.video_dimension[1])
        self.is_on = True

    def set_off(self):
        self.is_on = False
        print('camera setting off')
        self.camera = None
        assert(self.camera is None)


    def set_ai_on(self):
        self.manager = get_manager(self.camera_name)
        try:
            self.manager.connect()
            assert(self.manager is not None)
        except:
            print('can not connect to queue manager')
            return
        try:
            exec('self.ai_queue = self.manager.%s()' % self.camera_name)
            assert(self.ai_queue is not None)
        except:
            print('can not get the ai queue')
            return
        self.send_data_to_ai = True


    def set_ai_off(self):
        if self.is_recording:
            self.ai_queue.put({
                'session_id': -1,
                'time_stamp': datetime.now(),
                'frame': None
            })
        self.send_data_to_ai = False
        self.manager = None
        self.ai_queue = None



    def stop_recording(self):
        print('Camera %s, total_frames: %s' % (self.camera_idx, self.frame_count))
        self.frame_count = 0
        if self.send_data_to_ai:
            self.ai_queue.put({
                'session_id': -1,
                'time_stamp': datetime.now(),
                'frame': None
            })
        self.is_recording = False

    def record(self):
        self.frame_count = 0
        if not self.is_on:
            print('You need to turn on the camera first')
            return
        self.is_recording = True
        while(self.is_on and self.is_recording):
            file_name = str(datetime.now()).replace(' ', '_') + '.avi'
            print('recording file: %s' % file_name)
            vw = cv2.VideoWriter(self.data_path + file_name, Camera.fourcc_code, Camera.frame_rate, Camera.video_dimension)
            for frame_idx in range(Camera.frame_count_interval):
                if self.camera is None or not self.is_on or not self.is_recording:
                    vw.release()
                    self.write_to_db(file_name)
                    return
                else:
                    success, frame = self.camera.read()
                    assert(success)
                    vw.write(frame)
                    self.frame_count += 1
                    if self.send_data_to_ai:
                        cur_time = datetime.now()
                        self.ai_queue.put({
                            'session_id': self.session_id,
                            'time_stamp': cur_time,
                            'frame': frame
                        })
            vw.release()
            self.write_to_db(file_name)


if __name__ == '__main__':
    c = Camera(0)
    c.set_on()
    c.set_ai_on()
    Thread(target=c.record).start()
    from time import sleep
    sleep(27)
    c.set_ai_off()
    c.set_off()







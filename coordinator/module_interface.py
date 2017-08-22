from database_service.video_writer import VideoWriter
from datetime import datetime
from threading import Thread
import requests

class CoordinatorModule:
    def __init__(self):
        self.session_id = -1
        self.camera_base_port = 14312
        self.vw = VideoWriter()
        CoordinatorModule.button_pressed = False


    def set_session_id(self, session_id):
        self.session_id = session_id

    def reset_button(self):
        CoordinatorModule.button_pressed = False


    def set_button(self):
        CoordinatorModule.button_pressed = True


    def get_button_status(self):
        return CoordinatorModule.button_pressed


    def write_video_to_database(self, file_name, camera_idx):
        file_path = '/home/salil/PycharmProjects/PodClient/data/' + str(camera_idx)
        file_path += '/%s' % file_name
        self.vw.write_task_to_db(datetime.now(), file_path, self.session_id, camera_idx)


    def start_recording(self, camera_list, session_id, ai=False):
        # Turn on both cameras first
        init = True
        for camera_idx in camera_list:
            name = 'camera' + str(camera_idx)
            port_num = self.camera_base_port + camera_idx
            base_url = 'http://localhost:%s/camera/%s/' % (port_num, name)
            set_on_url = base_url + 'set_on'
            requests.get(set_on_url)
            if ai:
                if init == False:
                    pass
                print('ai on')
                ai_on_url = base_url + 'ai_on'
                requests.get(ai_on_url)
                init = False

        # Start recoding
        for camera_idx in camera_list:
            name = 'camera' + str(camera_idx)
            port_num = self.camera_base_port + camera_idx
            base_url = 'http://localhost:%s/camera/%s/' % (port_num, name)
            record_url = base_url + 'record'
            Thread(target=requests.get, args=(record_url, )).start()

        if ai:
            print('ai called')
            Thread(target=requests.get,
                   args=('http://localhost:32766/create_session?session_id=%s&cameras=camera0,camera1' % session_id,)).start()


    def end_recording(self, camera_list, ai=False):
        for camera_idx in camera_list:
            name = 'camera' + str(camera_idx)
            port_num = self.camera_base_port + camera_idx
            base_url = 'http://localhost:%s/camera/%s/' % (port_num, name)
            stop_url = base_url + 'stop_recording'
            Thread(target=requests.get, args=(stop_url,)).start()
        init = True
        for camera_idx in camera_list:
            name = 'camera' + str(camera_idx)
            port_num = self.camera_base_port + camera_idx
            base_url = 'http://localhost:%s/camera/%s/' % (port_num, name)
            if ai:
                if init == False:
                    pass
                ai_off_url = base_url + 'ai_off'
                requests.get(ai_off_url)
                init = False
            set_off_url = base_url + 'set_off'
            requests.get(set_off_url)




if __name__ == '__main__':
    c = CoordinatorModule()
    c.start_recording([0, 1])
    from time import sleep
    sleep(16)
    c.end_recording([0, 1])



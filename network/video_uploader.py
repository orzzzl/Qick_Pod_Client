from network.ai_server import *
from database_service.video_writer import VideoWriter
from threading import Thread
from time import sleep


class VideoUploader():
    def __init__(self):
        self._video_writer = VideoWriter()
        self.working = False
        Thread(target=self.work).start()
        self.set_on()

    def process_file(self, f, s, c):
        print('uploading: %s' % f)
        upload(f, s, c)
        print('end uploading %s' % f)
        self._video_writer.set_complete(f)

    def set_on(self):
        print('uploader is on')
        self.working = True


    def set_off(self):
        print('uploader is off')
        self.working = False

    def work(self):
        print('upload worker start working')
        while True:
            if not self.working:
                continue
            tasks = []
            to_dos = self._video_writer.get_all_tasks(0)

            for entity in to_dos:
                t = Thread(target=self.process_file, args=(entity['file_path'], entity['session_id'], entity['camera_idx']))
                tasks.append(t)

            for t in tasks:
                t.start()

            for t in tasks:
                t.join()

            sleep(1)

if __name__ == '__main__':
    from datetime import datetime
    create_session(888, datetime.now())
    vu = VideoUploader()
    from time import sleep
    sleep(5)
    vu.set_on()
    sleep(20)

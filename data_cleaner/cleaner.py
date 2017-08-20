from database_service.video_writer import VideoWriter
from time import sleep
from threading import Thread
import os

class Cleaner:
    def __init__(self):
        self._vw = VideoWriter()
        self.is_cleaning_on = False
        Thread(target=self.work).start()
        self.set_on()


    def work(self):
        print('cleaner starts working.')
        while True:
            if not self.is_cleaning_on:
                continue
            sleep(1)
            to_be_cleaned = self._vw.get_all_tasks(1)
            for entity in to_be_cleaned:
                os.remove(entity['file_path'])
                self._vw.clear_finished_task(entity['file_path'])

    def set_on(self):
        self.is_cleaning_on = True

    def set_off(self):
        self.is_cleaning_on = False
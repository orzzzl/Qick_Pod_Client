from time import sleep
from threading import Thread
from database_service.video_writer import VideoWriter
from network.ai_server import end_session


class EndSessionChecker:
    def __init__(self):
        self.is_on = False
        EndSessionChecker._sessions = set()
        EndSessionChecker._vw = VideoWriter()
        EndSessionChecker._session_to_data = {}
        Thread(target=self.work).start()
        self.set_on()


    def add_session_data(self, session_id, data):
        print('session_data_added: ' + str(session_id))
        EndSessionChecker._session_to_data[session_id] = data

    def add_session(self, session_id):
        print('session_added: ' + str(session_id))
        EndSessionChecker._sessions.add(session_id)

    def remove_session(self, session_id):
        print('session removed: ' + str(session_id))
        EndSessionChecker._sessions.remove(session_id)
        del EndSessionChecker._session_to_data[session_id]

    def set_on(self):
        print('setting esc on')
        self.is_on = True

    def set_off(self):
        print('setting esc off')
        self.is_on = False

    def work(self):
        print("End Session Checker starts working.")
        while True:
            if not self.is_on:
                continue
            sleep(0.77)
            to_be_removed = []
            for s in EndSessionChecker._sessions:
                if s >= 0:
                    res = EndSessionChecker._vw.get_all_tasks_by_session(0, s)
                    if len(res) == 0:
                        print('session uploaded:', s)
                        print('session uploaded:' + str(s))
                        to_be_removed.append(s)
                        end_session(EndSessionChecker._session_to_data[s])

            for s in to_be_removed:
                self.remove_session(s)
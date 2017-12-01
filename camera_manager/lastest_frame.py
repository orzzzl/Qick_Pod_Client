from multiprocessing import Queue
import sys

class LatestFrame0:
    frame = None
    session_id = -1
    framequeue = Queue()
    depthqueue = Queue()
    ai_framequeue = Queue()

    @classmethod
    def get_session_id(cls):
        return LatestFrame0.session_id

    @classmethod
    def get(cls):
        return LatestFrame0.framequeue.get()

    @classmethod
    def get_depth(cls):
        return LatestFrame0.depthqueue.get()

    @classmethod
    def get_latest(cls):
        return LatestFrame0.frame

    @classmethod
    def set(cls, f, d):
        LatestFrame0.frame = {
            'frame': f,
            'depth': d,
            'session_id': LatestFrame0.session_id
        }
        LatestFrame0.framequeue.put(f)
        if LatestFrame0.framequeue.qsize() > 3:
            LatestFrame0.framequeue.get()
        LatestFrame0.depthqueue.put(d)
        if LatestFrame0.depthqueue.qsize() > 3:
            LatestFrame0.depthqueue.get()

    @classmethod
    def set_session_id(cls, id):
        LatestFrame0.session_id = id



    @classmethod
    def set_ai(cls, f, d):
        LatestFrame0.ai_framequeue.put({
            'frame': f,
            'depth': d,
            'session_id': LatestFrame0.session_id
        })

    @classmethod
    def get_ai(cls):
        return LatestFrame0.ai_framequeue.get()


class LatestFrame1:
    frame = None
    session_id = -1
    framequeue = Queue()
    depthqueue = Queue()
    ai_framequeue = Queue()

    @classmethod
    def get_session_id(cls):
        return LatestFrame1.session_id

    @classmethod
    def get(cls):
        return LatestFrame1.framequeue.get()

    @classmethod
    def get_depth(cls):
        return LatestFrame1.depthqueue.get()

    @classmethod
    def set(cls, f, d):
        LatestFrame1.frame = {
            'frame': f,
            'depth': d,
            'session_id': LatestFrame1.session_id
        }
        LatestFrame1.framequeue.put(f)
        if LatestFrame1.framequeue.qsize() > 3:
            LatestFrame1.framequeue.get()
        LatestFrame1.depthqueue.put(d)
        if LatestFrame1.depthqueue.qsize() > 3:
            LatestFrame1.depthqueue.get()

    @classmethod
    def set_session_id(cls, id):
        LatestFrame1.session_id = id

    @classmethod
    def set_ai(cls, f, d):
        LatestFrame1.ai_framequeue.put({
            'frame': f,
            'depth': d,
            'session_id': LatestFrame1.session_id
        })

    @classmethod
    def get_latest(cls):
        return LatestFrame1.frame


    @classmethod
    def get_ai(cls):
        return LatestFrame1.ai_framequeue.get()


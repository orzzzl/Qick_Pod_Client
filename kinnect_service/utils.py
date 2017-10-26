from camera_manager.queue_manager import QueueManager

m = QueueManager.create_manager()
m.connect()
lf = m.LatestFrame0()
rf = m.LatestFrame1()

def set_session_id(id):
    lf.set_session_id(id)
    rf.set_session_id(id)

def end_session():
    set_session_id(-1)
    lf.set_ai(None, None)
    rf.set_ai(None, None)
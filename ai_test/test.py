from camera_manager.main import get_manager
import cv2
from datetime import datetime


name = 'camera1'
m = get_manager(name)
m.connect()
q = None
q = getattr(m , name)()
assert q is not None
file_name = str(datetime.now()).replace(' ', '_') + '.avi'
vw = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*'H264'), 15.0, (320, 240))
while(True):
    frame = q.get()
    vw.write(frame['frame'])
from flask import Flask
from flask import request
from threading import Thread
import requests
from network.commercial_server import *
from coordinator.module_interface import CoordinatorModule
app = Flask(__name__)


port = 14310
pod_id = 1
cm = CoordinatorModule()

@app.route('/coordinator/write_file_to_db')
def write_file_to_db():
    file_name = request.args.get('file_name')
    camera_idx = request.args.get('camera_idx')
    cm.write_video_to_database(file_name, camera_idx)
    return 'success'

@app.route('/coordinator/set_session_id')
def set_id():
    session_id = request.args.get('session_id')
    cm.set_session_id(session_id)
    return 'success'


@app.route('/coordinator/start_recording')
def start_recording():
    try:
        session_id = request.args.get('session_id')
        print('get session %s' % session_id)
    except:
        return 'false'
    camera_list = request.args.get('camera_list')
    map_obj = map(int, camera_list.split(','))
    cams = []
    for camera in map_obj:
        cams.append(camera)
    cm.start_recording(cams, ai=False)
    return 'success'


@app.route('/coordinator/end_recording')
def end_recording():
    camera_list = request.args.get('camera_list')
    map_obj = map(int, camera_list.split(','))
    cams = []
    for camera in map_obj:
        cams.append(camera)
    cm.end_recording(cams, ai=False)
    return 'success'


if __name__ == '__main__':
    app.run(port=port)

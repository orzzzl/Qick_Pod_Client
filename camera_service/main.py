from flask import Flask
import argparse
from camera_service.kinnect_service import Camera
from threading import Thread
app = Flask(__name__)


camera_idx = 0
parser = argparse.ArgumentParser()
parser.add_argument('--camera_idx')
args = parser.parse_args()
camera_idx = int(args.camera_idx)
camera_name = 'camera%s' % camera_idx
url_prefix = '/camera/%s/' % camera_name

url_hello = url_prefix + 'hello'
url_set_on = url_prefix + 'set_on'
url_set_off = url_prefix + 'set_off'
url_ai_on = url_prefix + 'ai_on'
url_ai_off = url_prefix + 'ai_off'
url_record = url_prefix + 'record'
url_stop_recording = url_prefix + 'stop_recording'

web_cam = Camera(camera_idx)

port = 14312 + camera_idx

@app.route(url_hello)
def hello_world():
    return 'Hello World from camera_service: ' +  camera_name

@app.route(url_set_on)
def set_on():
    if web_cam.is_on:
        return 'camera is on already'
    else:
        web_cam.set_on()
        return 'camera is now turned on'

@app.route(url_set_off)
def set_off():
    if not web_cam.is_on:
        return 'camera is off already'
    else:
        web_cam.set_off()
        return 'camera is now turned off'


@app.route(url_ai_on)
def ai_on():
    if web_cam.send_data_to_ai:
        return 'ai is already on'
    else:
        web_cam.set_ai_on()
        return 'ai is now turned on'


@app.route(url_ai_off)
def ai_off():
    if not web_cam.send_data_to_ai:
        return 'ai is already off'
    else:
        web_cam.set_ai_off()
        return 'ai is now turned off'

@app.route(url_record)
def record():
    if web_cam.is_recording:
        return 'camera is already recording'
    else:
        Thread(target=web_cam.record).start()
        return 'camera is now recording'

@app.route(url_stop_recording)
def stop_recording():
    if not web_cam.is_recording:
        return 'camera is not recording already'
    else:
        web_cam.stop_recording()
        return 'camera is now stopping recording'

if __name__ == '__main__':
    app.run(port=port)

from flask import Flask
from flask import request
from network.ai_server import *
from network.video_uploader import VideoUploader
app = Flask(__name__)


port = 14309
vu = VideoUploader()

@app.route('/uploader/set_on')
def set_on():
    vu.set_on()
    return 'success'


@app.route('/uploader/set_off')
def set_off():
    vu.set_off()
    return 'success'


@app.route('/uploader/create_session')
def open_session():
    session_id = request.args.get('session_id')
    start_time = request.args.get('start_time')
    create_session(session_id, start_time)
    return 'success'







if __name__ == '__main__':
    app.run(port=port)

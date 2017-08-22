import requests
from threading import Thread
from network.commercial_server import *
import select
import sys
from time import sleep

cameras = '0,1'
session_status = 'FINISHED'
session_id = -1
pod_id = 1
dis_able_door = False
start_time = None

def start_recording(session_id):
    start_url = 'http://127.0.0.1:14310/coordinator/start_recording?camera_list=%s&session_id=%s' % (cameras, session_id)
    Thread(target=requests.get, args=(start_url, )).start()

def end_recording(session_id):
    end_url = 'http://127.0.0.1:14310/coordinator/end_recording?camera_list=%s&session_id=%s' % (cameras, session_id)
    Thread(target=requests.get, args=(end_url, )).start()


def open_door():
    if dis_able_door:
        return
    url = 'http://127.0.0.1:14308/gpio/open_door'
    requests.get(url)

def close_door():
    if dis_able_door:
        return
    url = 'http://127.0.0.1:14308/gpio/close_door'
    requests.get(url)

def create_ai_session(session_id, start_time):
    url = 'http://127.0.0.1:14309/uploader/create_session?session_id=%s&start_time=%s' % (session_id, start_time)
    Thread(target=requests.get, args=(url, )).start()

def set_id(session_id):
    url = 'http://127.0.0.1:14310/coordinator/set_session_id?session_id=%s' % session_id
    requests.get(url)


def clear_input(stream, timeout=0):
    while stream in select.select([stream], [], [], timeout)[0]:
        stream.readline()

def add_esc(session_id, data):
    session_id = int(session_id)
    url = 'http://127.0.0.1:14306/esc/add_session?session_id=%s' % session_id
    requests.get(url)
    post_url = 'http://127.0.0.1:14306/esc/post_session_data'
    post_data = {
        'd': json.dumps(data),
        'session_id': session_id
    }
    requests.post(post_url, data = post_data)

while True:
    if session_status == 'FINISHED':
        clear_input(sys.stdin)
        line = input()
        line = line.strip()
        res = create_session(line, pod_id)
        if res['open_door']:
            session_id = res['shopping_session']['id']
            set_id(session_id)
            print('get session id: %s' % session_id)
            session_status = "WAIT_PPL"
            start_time_json = get_current_time_json()
            start_time = get_current_time()
            print('started')
            start_recording(session_id)
            open_door()
            create_ai_session(session_id, start_time_json)

    if session_status == 'WAIT_PPL':
        sleep(5)
        close_door()
        requests.get('http://localhost:14310/coordinator/reset_button')
        session_status = 'STARTED'

    if session_status == 'STARTED':
        sleep(0.5)
        status = requests.get('http://localhost:14310/coordinator/get_button_status')
        status = status.text
        if status == 'False':
             res = get_session(session_id)
        else:
            session_status = 'CLOSING'
            pay_session(session_id)
            continue
        if res['status'] == 'CLOSING':
            session_status = 'CLOSING'

    if session_status == 'CLOSING':
        open_door()
        sleep(5)
        close_door()
        leave_session(session_id)
        end_time = get_current_time()
        print(end_time)
        duration = (end_time - start_time).total_seconds()
        data = {
            'session_id': session_id,
            'end_time': end_time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'duration': str(duration),
            'cameras': '[%s]' % cameras
        }
        print(data)
        add_esc(session_id, data)
        end_recording(session_id)
        session_id = -1
        session_status = 'FINISHED'








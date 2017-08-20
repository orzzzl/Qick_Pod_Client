import requests
from random import randint


AI_SERVER_ADDRESS = '128.122.20.233'
PORT = 8000
http_address = 'http://' + AI_SERVER_ADDRESS + ':' + str(PORT)


def upload(file_path, session_id, camera_idx):
    data = {
        'session_id': session_id,
        'camera_idx': camera_idx
    }
    file_name = file_path.split('/')[-1]
    url = http_address + '/upload'
    files = {
        file_name: open(file_path, 'rb')
    }
    r = requests.post(url, files=files, data=data)
    return r



def create_session(session_id, start_time):
    data = {
        'start_time': start_time,
        'customer_id': randint(0, 11),
        'session_id': session_id,
        'pod_id': 1
    }
    print('ai server create session with data', data)
    url = http_address + '/createsession'
    r = requests.post(url, data)
    print(r)


def end_session(data):
    url = http_address + '/endsession'
    requests.post(url, data)
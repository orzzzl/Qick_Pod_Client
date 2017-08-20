import requests
import json
from datetime import datetime

COMMERCIAL_SERVER_ADDRESS = '104.131.73.233:8080'
http_address = 'http://' + COMMERCIAL_SERVER_ADDRESS
pod_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJxaWNrY3MiLCJ1aWQiOjEsInN1YiI6IlBPRCJ9.bqQFnZjewxo_dywXb89sPgVA-WzC5FgTZK98oxFrwtJWbWnFaxRj9b67WgIlAQWJyUGKR3MYgdM1V0BRMiHBo6xbmu0AWHAVw_32HSAmMA0sT0290KoBlEr65D5utkK7DvxdI3_GB39Qfq5zHAorYPAxQ8LcAtMUKhmrRgV6g32rnPNa5HHkAyaAXhztARefk-9ZDdFIWpj_7fnkV_vXfr297kWgajAn4JXPT76MO7RREjoSt-9kqDGBNB7qiBC4kFkF42unaAc9Q7JfiM95BBGP8C1hibBFCAs3YfViyQ7rGarFZkyclLx4sSu9Fj1P56Lt7pfCzpDeaInrKxDbUtbeWEi6y1eumatdC8SJebM9NMGrc40RE96nAYZgerz1K4KPQ30iB-ZDwPtAVNJ-N5h6cneey-N4Vhh6o1t1H0mq03-rwId8NixnA6ETcbD7On_JBzZcf0SLGdxSjsbwfRiy8NrymvQhdOucucIyAOhAdBKTg8SmR6vhqKVNhddko-Jz7zvXmJGp1K4NWfRXU6ezePVkaBpt-XhGRfMiiIlQBnsXjLhG-O99b9NxJUxBauYTcRb5PTVZakZpa9ZiBl-XauoYW3nd-qtUCFPmkIOko4HIhh8PiZA5hX8709bNPFMxd9VJOk8Uoz2J4dpElvv5jEd2fL1dGsox7aAYpeA'


def process_response(res):
    res_str = json.dumps(res.json())
    res_str = res_str.replace('false', 'False')
    res_str = res_str.replace('true', 'True')
    res_str = res_str.replace('null', 'None')
    return eval(res_str)


def create_session(hashed_str, pod_id):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % pod_token,
    }

    data = {
        'pod_id': pod_id,
        'key': hashed_str
    }

    r = requests.post(http_address + '/pods/verify', data=json.dumps(data), headers=headers)
    return process_response(r)


def pay_session(session_id):
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % pod_token,
        'Content-Type': 'application/json'
    }
    r = requests.post(http_address + '/shopping/sessions/%s/pay' % session_id, headers=headers)
    return process_response(r)


def get_session(session_id):
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % pod_token,
        'Content-Type': 'application/json'
    }
    r = requests.get(http_address + '/shopping/sessions/%s' % session_id, headers=headers)
    return process_response(r)


def get_current_time():
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % pod_token,
        'Content-Type': 'application/json'
    }
    r = requests.get(http_address + '/server/time', headers=headers)
    return datetime.strptime(str(r.json()['time']), '%Y-%m-%dT%H:%M:%S.%f')


def get_current_time_json():
    r = requests.get(http_address + '/server/time')
    return r.json()['time']


def update_ai_count(ai_count, session_id):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % pod_token,
    }

    data = {
        'ai_item_count': ai_count
    }

    r = requests.put(http_address + '/shopping/sessions/%s/ai_item_count' % session_id, data=json.dumps(data), headers=headers)
    return process_response(r)

def leave_session(session_id):
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % pod_token,
        'Content-Type': 'application/json'
    }
    r = requests.post(http_address + '/shopping/sessions/%s/finish' % session_id, headers=headers)
    return process_response(r)
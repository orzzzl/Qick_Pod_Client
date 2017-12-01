from flask import Flask
from flask import request
from end_session_checker.esc import EndSessionChecker
import json
app = Flask(__name__)


port = 14306
my_esc = EndSessionChecker()

@app.route('/esc/add_session')
def add_session():
    session_id = request.args.get('session_id')
    my_esc.add_session(int(session_id))
    return 'success'

@app.route('/esc/remove_session')
def close_door():
    session_id = request.args.get('session_id')
    my_esc.remove_session(session_id)
    return 'success'

@app.route('/esc/post_session_data', methods=['POST'])
def post_session_data():
    print('called')
    data = json.loads(request.form['d'])
    session_id = int(request.form['session_id'])
    print(data)
    print(session_id)
    my_esc.add_session_data(session_id, data)
    return 'success'

@app.route('/esc/set_on')
def set_on():
    my_esc.set_on()
    return 'success'

@app.route('/esc/set_off')
def set_off():
    my_esc.set_off()
    return 'success'


if __name__ == '__main__':
    app.run(port=port)

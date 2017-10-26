from flask import Flask
from gpio_service.door import Door
app = Flask(__name__)


port = 14308
my_door = Door()

@app.route('/gpio/open_door')
def open_door():
    my_door.open_door()
    return 'success'

@app.route('/gpio/close_door')
def close_door():
    my_door.close_door()
    return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

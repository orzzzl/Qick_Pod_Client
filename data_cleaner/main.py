from flask import Flask
from data_cleaner.cleaner import Cleaner
app = Flask(__name__)


port = 14307
my_cleaner = Cleaner()

@app.route('/clean/set_on')
def set_on():
    my_cleaner.set_on()
    return 'success'

@app.route('/gpio/close_door')
def set_off():
    my_cleaner.set_off()
    return 'success'

if __name__ == '__main__':
    app.run(port=port)

import requests
import json

from flask import (Flask, url_for, redirect)
from flask import (render_template, request)


app = Flask(__name__)
app.config.from_object('config')

# zero entry is not used
led_list = [{'led_id': i, 'brightness': 0} for i in range(1, 19)]
ARM_LED_LIST = map(tuple, ([{'led_id': i, 'brightness': 0} for i in range(1, 7)],
                           [{'led_id': i, 'brightness': 0} for i in range(7, 13)],
                           [{'led_id': i, 'brightness': 0} for i in range(13, 19)]))

PG_SERVER = 'http://192.168.2.124:5000'
#PG_SERVER = 'http://localhost:5000'

def make_url(path, *args):
    root = app.config.get('PG_SERVER', 'http://localhost:5000')
    return root + path % args

@app.route('/', methods=['GET', ])
def show_control():
    return render_template('control.html', led_list=led_list, arm_list=ARM_LED_LIST)


@app.route('/set_led', methods=['POST', ])
def set_led():
    """
    Set single LED
    """
    print request.form
    n = int(request.form.get('led_id'))
    v = request.form.get('brightness', 100)
    data = {'brightness': v}
    r = requests.put(make_url('/leds/%d', n), data=data)
    print r

    return redirect(url_for('show_control'))


@app.route('/set_leds', methods=['POST', ])
def set_leds():
    """
    Set multiple LEDs at the same time
    """
    data = []
    for i in range(1, 19):
        v = int(request.form.get('led_%d' % i, 0))
        d = {'led_id': i, 'brightness': v}
        data.append(d)

    print data
    r = requests.put(make_url('/leds'), data=json.dumps(data),
                     headers={'content-type': 'application/json'})
    print r

    return redirect(url_for('show_control'))


@app.route('/set_arms', methods=['POST', ])
def set_arms():
    ids = []
    for i in range(1, 3):
        v = request.form.get('arm_%d' % i, 0)
        data = {'brightness': v}
        r = requests.put(make_url('/arms/%d', i), data=data)
        print r
        print i, v

    return redirect(url_for('show_control'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

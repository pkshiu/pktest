import requests

from flask import (Flask, url_for, redirect)
from flask import (render_template, request)


app = Flask(__name__)
app.config.from_envvar('PGS_SETTINGS', silent=True)

# zero entry is not used
led_list = [{'led_id': i, 'brightness': 0} for i in range(0, 20)]
ARM_LED_LIST = map(tuple, ([{'led_id': i, 'brightness': 0} for i in range(1, 7)],
                           [{'led_id': i, 'brightness': 0} for i in range(7, 13)],
                           [{'led_id': i, 'brightness': 0} for i in range(13, 19)]))

PG_SERVER = 'http://192.168.2.124:5000'
PG_SERVER = 'http://localhost:5000'


@app.route('/', methods=['GET', ])
def show_control():
    return render_template('control.html', led_list=led_list, arm_list=ARM_LED_LIST)


@app.route('/set_leds', methods=['POST', ])
def set_leds():
    ids = []
    for i in range(1, 19):
        v = request.form.get('led_%d' % i, 0)
        data = {'brightness': v}
        r = requests.put('%s/leds/%d' % (PG_SERVER, i), data=data)
        print i, v

    return redirect(url_for('show_control'))


if __name__ == '__main__':
    print led_list
    app.run(debug=True, host='0.0.0.0', port=8000)

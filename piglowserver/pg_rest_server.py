"""
    This is a REST server that accept requests to control the PiGlow board.

    A few interesting things about this server:
    * It is designed with a RESTful Api
    * It uses a global lock to queue up operations to the PiGlow
"""
import threading
import time

from flask import Flask
from flask import (render_template, request)
from flask.ext.restful import (Resource, Api)

# Support a dummy PyGlow class so that we can test this code
# on something other than a real RPi
try:
    from PyGlow import (PyGlow, ARM_LED_LIST)
except ImportError:
    from dummy_pyglow import (PyGlow, ARM_LED_LIST)


pyglow = PyGlow()

app = Flask(__name__)
app.config.from_envvar('PGS_SETTINGS', silent=True)
api = Api(app)

# zero entry is not used
led_list = [{'led_id': i, 'brightness': 0} for i in range(0, 20)]

# global lock
lock = threading.Lock()


# interface to the h/w layer
def set_led(num, brightness):
    """
    Set one LED

    :param num: is the LED number, from 1 to 18
    :param brightness: is the light level, from 0-255
    """
    global lock

    # do this one at a time
    with lock:
        led_list[num]['brightness'] = brightness
        pyglow.led(num, brightness=brightness)


def set_arm(num, brightness):
    """
    Set one arm of the PiGlow

    :param num: is the arm number, from 1 to 3
    :param brightness: is the light level, from 0-255
    """
    global lock

    # do this one at a time
    with lock:
        for i in ARM_LED_LIST[num - 1]:
            led_list[i]['brightness'] = brightness
        pyglow.arm(num, brightness=brightness)


# interface to the h/w layer
def set_leds(set_list):
    """
    Set list of LED

    :param set_list: is a list of (id, brightness)
    """
    global lock

    # do this one at a time
    with lock:
        for num, b in set_list:
            led_list[num]['brightness'] = b
            pyglow.led(num, brightness=b)


class LedListAPI(Resource):
    """
        REST interface to get the LED list.
    """
    def get(self):
        return led_list

    def put(self):
        """
        Accept JSON [ {id:n, brightness:b}, ...]
        """
        print 'LedList PUT'
        print request.json
        set_list = []
        for d in request.json:
            n = d['id']
            v = d['brightness']
            set_list.append((n, v))

        # call set_led(led_id, v) but in a separate thread
        h = threading.Thread(target=set_leds, args=(set_list,))
        h.setDaemon(True)
        h.start()

        return led_list


class LedAPI(Resource):
    """
        REST interface to control the LEDs.
    """
    def get(self, led_id):
        return led_list[led_id]

    def put(self, led_id):
        print 'Led PUT'
        print request.form
        v = request.form['brightness']
        print 'value...', v
        v = int(v)

        # call set_led(led_id, v) but in a separate thread
        h = threading.Thread(target=set_led, args=(led_id, v))
        h.setDaemon(True)
        h.start()

        return led_list[led_id]


class ArmAPI(Resource):
    def get(self, arm_id):
        return led_list

    def put(self, arm_id):
        print 'putting ARM...'
        print request.form
        v = request.form['brightness']
        print 'value...', v
        v = int(v)

        h = threading.Thread(target=set_arm, args=(arm_id, v))
        h.setDaemon(True)
        h.start()

        return led_list

api.add_resource(LedAPI, '/leds/<int:led_id>')
api.add_resource(LedListAPI, '/leds')

api.add_resource(ArmAPI, '/arms/<int:arm_id>')
# api.add_resource(LedListAPI, '/leds')


@app.route('/')
def show_control():
    return render_template('control.html', led_list=led_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import (Flask, url_for, redirect)
from flask import (render_template, request)
from flask.ext.restful import (Resource, Api)

from PyGlow import (PyGlow, ARM_LED_LIST)
from time import sleep

pyglow = PyGlow()

app = Flask(__name__)
app.config.from_envvar('PGS_SETTINGS', silent=True)
api = Api(app)

# zero entry is not used
led_list = [{'led_id': i, 'brightness': 0} for i in range(0,20)]


# interface to the h/w layer
def set_led(num, brightness):
    led_list[num]['brightness'] = brightness
    pyglow.led(num, brightness=brightness)
#    pyglow.update_leds()

def set_arm(num, brightness):
    for i in ARM_LED_LIST[num-1]:
        led_list[i]['brightness'] = brightness
    pyglow.arm(num, brightness=brightness)
#    pyglow.update_leds()

class LedListAPI(Resource):
    def get(self):
        return led_list


class LedAPI(Resource):
    def get(self, led_id):
        return led_list[led_id]

    def put(self, led_id):
        print 'putting...'
        print request.form
        v = request.form['brightness']
        print 'value...', v
        v = int(v)
        set_led(led_id, v)
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
        set_arm(arm_id, v)
        return led_list

api.add_resource(LedAPI, '/leds/<int:led_id>')
api.add_resource(LedListAPI, '/leds')

api.add_resource(ArmAPI, '/arms/<int:arm_id>')
# api.add_resource(LedListAPI, '/leds')

@app.route('/')
def show_control():
    return render_template('control.html', led_list=led_list)



if __name__ == '__main__':
    print led_list
    app.run(debug=True, host='0.0.0.0')

from flask import (Flask, url_for, redirect)
from flask import (render_template, request)
from flask.ext.restful import (Resource, Api)


app = Flask(__name__)
app.config.from_envvar('PGS_SETTINGS', silent=True)
api = Api(app)

# zero entry is not used
led_list = [{'led_id': i, 'brightness': 0} for i in range(0,20)]


# interface to the h/w layer
def set_led(num, brightness):
    led_list[led_id]['brightness'] = v

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
        set_led(led_id, v)
        return led_list[led_id]

api.add_resource(LedAPI, '/leds/<int:led_id>')
api.add_resource(LedListAPI, '/leds')

@app.route('/')
def show_control():
    return render_template('control.html', led_list=led_list)



if __name__ == '__main__':
    print led_list
    app.run(debug=True, host='0.0.0.0')

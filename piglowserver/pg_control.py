from flask import (Flask, url_for, redirect)
from flask import (render_template, request)


app = Flask(__name__)
app.config.from_envvar('PGS_SETTINGS', silent=True)



@app.route('/')
def show_control():
    return render_template('control.html', led_list=led_list)



if __name__ == '__main__':
    print led_list
    app.run(debug=True, host='0.0.0.0', port=80)

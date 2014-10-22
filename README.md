Piglow Server
=============

This project has two parts:

1. A RESTful API server running on a RPi thas has a PiGlow board attached. This server will provide an interface for controlling the PiGlow remotely.

2. An example web server with a simple browser interface. You can run this on the same RPi, or on a completely different computer. It will control the PiGlow via the RESTful API server above.

By providing a web based API on the RPi to the PiGlow, we can move the application code to a different platform. For example your web store can use the API to send store product levels to the RPi via the web.

Technical Details
---------------------

This project also serves as an example for:

- running the Flask web framework on the RPi
- designing a RESTful API
- use thread locks to manipulate a shared resource (the PiGlow) on the RPi within a web server environment.
- using python unittest to test the API server


API Usage
---------

Example in using the API:

    # set arm 3 to brightness 50
    curl -X PUT -d brightness=50 http://localhost:5000/arms/3

    # switch on and off LED 7
    curl -X PUT -d brightness=100 http://localhost:5000/leds/7
    curl -X PUT -d brightness=0 http://localhost:5000/leds/7

    # switch on led 3 and 5 with brightness 10 and 200
    curl -X PUT -H 'Content-Type: application/json' \
        -d '[{"led_id":3, "brightness": 10}, {"led_id":5, "brightness":200 }]' \
        http://localhost:5000/leds

    # excute a starburst pattern
    curl -X PUT -d brightness=100 http://localhost:5000/patterns/starburst

    # turn everything off
    curl -X PUT http://localhost:5000/patterns/clear

Settings
------------

### API Server Location

By default the #web server# looks for the #API Server# at `http://localhost:5000` .
This is useful if you are running both the web server and the API server on the
same RPi. If you are running the web server on a different computer, you can
setup the address by using a local configuration file:

1. Create a local_config.py file
2. set the optional environment variable #PGS_SETTINGS# to point to that file:
` export PGS_SETTINGS=local_config.py `


Installation
-----------------------

### Prerequisite



LICENSE: MIT

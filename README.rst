Piglow Server
=============

This project has two parts:

1. A RESTful API server running on a RPi thas has a PiGlow board attached. This server will provide an interface for controlling the PiGlow remotely.

2. An example web server with a simple browser interface. You can run this on the same RPi, or on a completely different computer. It will control the PiGlow via the RESTful API server above.

Technical Details
---------------------

This project also serves as an example for:

- running the Flask web framework on the RPi
- designing a RESTful API
- use thread locks to manipulate a shared resource (the PiGlow) on the RPi within a web serve environment.



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

Developer Installation
-----------------------

LICENSE: MIT

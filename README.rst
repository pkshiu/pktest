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

LICENSE: MIT

Settings
------------

Developer Installation
-----------------------

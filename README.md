# Simple-Reverse-Shell
A basic reverse shell made with python to demonstrate possibilities for usage of client/server programming

To use locally (eg. on your own computer):
  - adjust the IP address ('host') in the client.py file to your own IP
  - adjust port on both server.py and client.py to any open port (default is set to 9999)
  - run server.py + client.py

To use remotely (eg. on a friends computer):
  - run server.py on your computer on some open port
  - run client.py on the other computer with your IP address in 'host' and port set to servers' port

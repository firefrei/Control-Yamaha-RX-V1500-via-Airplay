# Control Yamaha-RX-V1500 via Airplay
This tiny python3 script is made for media servers running an Airplay/Shairport-Server (e.g. Raspberry Pi). 
If any client connects to the airplay server it will send an RS232 command to a Yamaha RX-V1500 reciever and turn it on. After the client has disconnected it will turn the reciever off again.
It also provides a HTTP-API for controlling the receiver.

# Requirements
- Python 3
- python3 library 'serial' from pypi (use 'pip3 install pyserial')
- python3 library 'bottle' from pypi (use 'pip3 install bottle')
- Running Airplay/Shairport-Server (ask Dr. Google)
- Yamaha RX-V1500 A/V-Reciever
- RS232 card or USB dongle connected to the reciever

# Usage
- Clone and run with 'python3 main.py &'
- Done.

# How it works
The script listens on the airplay ports. If any client connects it will send the turn on command to the reciever and change it's input source to 'CD-R'.
The input source can be changed in file 'reciever_rs232.py'.
After two minutes without any connection it will try to turn the reciever off.

# Tests
The script was tested on a Raspberry Pi running Raspian and Shairport. It always worked fine with one connection, it is not tested for special scenarios (like more devices try to connect or similar). Use it on your own risk :-)
No guarantee the rs232 commands work fine and don't damage your device. I found them somewhere on the internet. Use it on your own risk :-)

# Autor
Matthias Frei - www.frei.media






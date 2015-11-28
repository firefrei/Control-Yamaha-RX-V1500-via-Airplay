from bottle import *
from reciever_rs232 import *

### FREI.media ###
### www.frei.media ###

@route('/api/power/<state>')
def power(state):
    if state != "state":
        new_state = bool(state)
        if new_state:
            recieverOn()
        else:
            recieverOffDirect()
        return str(new_state)

    return "-"


@route('/api/volume/<action>')
def volume(action):
    if action == "up":
        recieverVolume("up")
    else:
        recieverVolume("down")
    return str(True)


@route('/api/mute/<action>')
def volume(action):
    new_state = bool(action)
    if new_state:
        recieverMute(True)
    else:
        recieverMute(False)
    return str(True)


@route('/api/input-channel/<channel>')
def volume(channel):
    channel_list = list(["phono", "cd", "tuner", "cdr", "md-tape", "dvd", "dtv", "cbl-sat", "vcr1", "dvr-vcr2", "vaux"])
    if channel == "list":
        return str(channel_list)

    if channel in channel_list:
        return recieverInputChannel(channel)


def webserver(port):
    try:
        # Bottle webserver
        run(host='0.0.0.0', port=port)

    except KeyboardInterrupt:
        print("server stopped!")


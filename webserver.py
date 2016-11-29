from bottle import *
from reciever_rs232 import *

### FREI.media ###
### www.frei.media ###

@route('/api/power/<state>')
def power(state):
    if state != "state":
        new_state = str_to_bool(state)
        if new_state:
            recieverOn()
        else:
            recieverOffDirect()
        return str(new_state)

    return str(recieverStatus())


@route('/api/volume/<action>')
def volume(action):
    if not recieverStatus():
        return "ERROR"

    if action == "up":
        recieverVolume("up")
    else:
        recieverVolume("down")
    return str(True)


@route('/api/mute/<action>')
def mute(action):
    if not recieverStatus():
        return "ERROR"

    new_state = str_to_bool(action)
    if new_state:
        recieverMute(True)
    else:
        recieverMute(False)

    return str(new_state)


@route('/api/input-channel/<channel>')
def input_channel(channel):
    if not recieverStatus():
        return "ERROR"
        
    channel_list = list(["phono", "cd", "tuner", "cdr", "md-tape", "dvd", "dtv", "cbl-sat", "vcr1", "dvr-vcr2", "vaux"])
    if channel == "list":
        return str(channel_list)

    if channel in channel_list:
        return recieverInputChannel(channel)


def str_to_bool(s):
    if s == 'True' or s == 'true' or s == '1':
        return True
    else:
        return False


def webserver(port):
    try:
        # Bottle webserver
        run(host='0.0.0.0', port=port)

    except KeyboardInterrupt:
        print("server stopped!")


if __name__ == "__main__":
    webserver(1888)

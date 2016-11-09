from reciever_rs232 import *
import argparse
import os
import sys


### FREI.media ###
### www.frei.media ###

def power(state=False):
    if state == "state":
        # turn off log outputs
        sysstdout_null = open(os.devnull, 'w')
        sysstdout_org = sys.stdout
        sys.stdout = sysstdout_null
        cur_state = recieverStatus()
        sys.stdout = sysstdout_org

        if cur_state is True:
            return 'on'
        else:
            return 'off'
    elif state == 'on':
        recieverOn()
        return str(state)
    elif state == 'off':
        recieverOffDirect()
        return str(state)
    else:
        return "ERROR: unknown state"


def volume(state):
    if state == "up":
        recieverVolume("up")
    else:
        recieverVolume("down")
    return str(True)


def mute(state):
    if state == 'on':
        recieverMute(True)
        return str(state)
    elif state == 'off':
        recieverMute(False)
        return str(state)
    else:
        return "ERROR: unknown state"


def input_channel(channel):
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


FUNCTION_MAP = {'power' : power,
                'volume' : volume,
                'mute' : mute,
                'input' : input_channel }

# Parse arguments
parser = argparse.ArgumentParser(description="Control RX-V1500 via Command Line Interface")
parser.add_argument('action', help='The action to take (e.g. power, volume, channel.)', choices=FUNCTION_MAP.keys())
parser.add_argument('value', help='New value (e.g. on, off, up, down)')
args = parser.parse_args()


# Execute action
func = FUNCTION_MAP[args.action]
result = func(args.value)
print(result)


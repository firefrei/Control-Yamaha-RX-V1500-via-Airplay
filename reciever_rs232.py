import serial
import multiprocessing
from time import sleep

### FREI.media ###
### www.frei.media ###


RECIEVER_OFF_WAIT = 120  # seconds to wait before turning off reciever
countdown_threads = list()
CONNECTION = serial.Serial()  # RS232-Connection

def openConnection():
    global CONNECTION

    if CONNECTION.isOpen() is False:
        CONNECTION = initConnection()
        if CONNECTION.isOpen():
            return CONNECTION
        else:
            return False
    else:
        return CONNECTION


def initConnection():
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0,
                        rtscts=0)
    # ser.open()
    device_is_responing = False
    if ser.isOpen():
        global device_is_responing
        while not device_is_responing:
            ser.write(b'\x11' + "000".encode() + b'\x03')
            response = ser.read(200)
            if response.find(b'\x03'):
                device_is_responing = True
                break
            else:
                print("Did not receive any response. Trying again...")
            sleep(1)
        print("Connection is open.")
    else:
        return False
    return ser


def formatCommand(command):
    return bytes([2]) + command.encode() + bytes([3])


def recieverOn():
    ser = openConnection()

    # Stop turn off timers
    if countdown_threads:
        for timer in countdown_threads:
            timer.terminate()

    print("Send command to TURN ON...")
    # Turn on
    ser.write(formatCommand("07a1d"))

    # Change input chanel to DVR-VCR2
    ser.write(formatCommand("07a13"))


def recieverOff():
    # Stop other timers
    if countdown_threads:
        for timer in countdown_threads:
            timer.terminate()

    # start new timer
    countdown = multiprocessing.Process(target=recieverOffCountdown, args=(RECIEVER_OFF_WAIT,))
    countdown.start()
    countdown_threads.append(countdown)


def recieverOffDirect():
    ser = openConnection()

    print("Send command to TURN OFF...")
    ser.write(formatCommand("07a1e"))

    print("Finished. Closing connection...")
    ser.close()


def recieverOffCountdown(seconds):
    print("Countdown started to TURN OFF in " + str(seconds) + "seconds...")
    while seconds > 0:
        seconds -= 1
        sleep(1)
    recieverOffDirect()


def recieverVolume(action):
    ser = openConnection()

    if action == "up":
        print("Send command to VOLUME UP...")
        ser.write(formatCommand("07a1a")+formatCommand("07a1a")+formatCommand("07a1a"))
    else:
        print("Send command to VOLUME DOWN...")
        ser.write(formatCommand("07a1b")+formatCommand("07a1b")+formatCommand("07a1b"))


def recieverMute(action=True):
    ser = openConnection()

    if action:
        print("Send command to MUTE...")
        ser.write(formatCommand("07ea2"))
    else:
        print("Send command to NOT MUTE...")
        ser.write(formatCommand("07ea3"))


def recieverInputChannel(channel):
    code = ""
    if channel == "phono":
        code = "07a14"
    elif channel == "cd":
        code = "07a15"
    elif channel == "tuner":
        code = "07a16"
    elif channel == "cdr":
        code = "07a19"
    elif channel == "md-tape":
        code = "07ac9"
    elif channel == "dvd":
        code = "07ac1"
    elif channel == "dtv":
        code = "07a54"
    elif channel == "cbl-sat":
        code = "07ac0"
    elif channel == "vcr1":
        code = "07a0f"
    elif channel == "dvr-vcr2":
        code = "07a13"
    elif channel == "vaux":
        code = "07a55"

    if code:
        ser = openConnection()
        print("Send command to SWITCH CHANNEL...")
        ser.write(formatCommand(code))
        return True
    else:
        return False


"""
Known commands:
------------------------------
InputPhono = "07a14",
InputCD = "07a15",
InputTuner = "07a16",
InputCDR = "07a19",
InputMD_TAPE = "07ac9",
InputDVD = "07ac1",
InputDTV = "07a54",
InputCBL_SAT = "07ac0",
InputVCR1 = "07a0f",
InputDVR_VCR2 = "07a13",
InputVAUX = "07a55",
MasterVolumeUp = "07a1a",
MasterVolumeDown = "07a1b",
AudioMuteOn = "07ea2",
AudioMuteOff = "07ea3",
PureDirectOn = "07e80",
PureDirectOff = "07e82",
SixChInputOn = "07ea4",
SixChInputOff = "07ea5",
InputModeAuto = "07ea6",
InputModeDDRF = "07ea7",
InputModeDTS = "07ea8",
InputModeDigital = "07ea9",
InputModeAnalog = "07eaa",
InputModeAAC = "07e3b",
Zone2VolumeUp = "07ada",
Zone2VolumeDown = "07adb",
Zone2MuteOn = "07ea0",
Zone2MuteOff = "07ea1",
Zone2InputPhono = "07ad0",
Zone2InputCD = "07ad1",
Zone2InputTuner = "07ad2",
Zone2InputCDR = "07ad4",
Zone2InputMD_TAPE = "07acf",
Zone2InputDVD = "07acd",
Zone2InputDTV = "07ad9",
Zone2InputCBL_SAT = "07acc",
Zone2InputVCR1 = "07ad6",
Zone2InputDVR_VCR2 = "07ad7",
Zone2InputVAUX = "07ad8",
PowerOn = "07a1d",
PowerOff = "07a1e",
Zone2PowerOn = "07eba",
Zone2PowerOff = "07ebb",
OSDOff = "07eb0",
OSDShort = "07eb1",
OSDFull = "07eb2",
SleepOff = "07eb3",
Sleep120 = "07eb4",
Sleep90 = "07eb5",
Sleep60 = "07eb6",
Sleep30 = "07eb7",
EX_ESOn = "07eb8",
EX_ESOff = "07eb9",
EX_ESAuto = "07e7c",
EX_ESDiscrete = "07e7d",
EX_ESDolbyEX = "07edc",
EX_ESPLIIxMovie = "07edd",
EX_ESPLIIxMusic = "07ede",
NightModeOff = "07e9c",
NightModeCinema = "07e9b",
NightModeMusic = "07ecf",
EffectOn = "07e27",
StereoStraight = "07ee0",
DSPHallE = "07ee5",
DSPJazz = "07eec",
DSPRock = "07eed",
DSPDisco = "07ef0",
DSPGame = "07ef2",
DSP7chStereo = "07eff",
DSPMusicVideo = "07ef3",
DSPMonoMovie = "07ef7",
DSPVarietySports = "07ef8",
DSPSpectacle = "07ef9",
DSPSciFi = "07efa",
DSPAdventure = "07efb",
DSPGeneral = "07efc",
DSPNormal = "07efd",
DSPEnhanced = "07efe",
DSPPLIIMovie = "07e67",
DSPPLIIMusic = "07e68",
DSPNeo6Cinema = "07e69",
DSPNeo6Music = "07e6a",
DSP2chDirectStereo = "07ec1",
DSP2chStereo = "07ec0",
DSPTHXCinema = "07ec2",
DSPPLIIGame = "07ec7",
TunerPageA = "07ae0",
TunerPageB = "07ae1",
TunerPageC = "07ae2",
TunerPageD = "07ae3",
TunerPageE = "07ae4",
TunerPreset1 = "07ae5",
TunerPreset2 = "07ae6",
TunerPreset3 = "07ae7",
TunerPreset4 = "07ae8",
TunerPreset5 = "07ae9",
TunerPreset6 = "07aea",
TunerPreset7 = "07aeb",
TunerPreset8 = "07aec",
TunerBandFM = "07ebc",
TunerBandAM = "07ebd",
AutoTuningUp = "07ebe",
AutoTuningDown = "07ebf",
SpeakerRelayAOn = "07eab",
SpeakerRelayAOff = "07eac",
SpeakerRelayBOn = "07ead",
SpeakerRelayBOff = "07eae",
SPBSetZone1 = "07e28",
SPBSetZone2 = "07e29",
Zone2SPOutOn = "07e99",
Zone2SPOutOff = "07e9a",
TunerFrequencyRequest = "22000",
"""

from airport_watcher import AirplayWatcher
from reciever_rs232 import *
from webserver import *

print("::.::.::.::.::.::.::")
print("FREI.media:home")
print("www.frei.media")
print("::.::.::.::.::.::.::")
print("\n")
print("//--- RX-V1500 Airport Actor ---\\")
print("// Copyright 2015 :.: All rights reserved \\")

print("\n\n")

try:
    print("Starting Airplay Watcher...")
    airplay_watcher = AirplayWatcher()
    airplay_watcher.setOnActivate(recieverOn)
    airplay_watcher.setOnDeactivate(recieverOff)
    airplay_watcher.start()
    webserver(1888)


except:
    print("Stopping Airplay Watcher...")
    airplay_watcher.stop()

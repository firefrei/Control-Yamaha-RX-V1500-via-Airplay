# Manage Airplay transmissions to shairport
# Source: http://www.raspberrypi.org/forums/viewtopic.php?f=38&t=37094&start=25

from threading import Thread
from time import sleep

PROC_TCP = "/proc/net/tcp"
AIRPLAY_POLLING_PERIOD = 0.5

class AirplayWatcher(Thread):
   def is_airplay_active(self):
      airplay_active = False
      with open(PROC_TCP,'r') as f:
         for line in f:
            elements = line.lstrip().split(' ')
            if (((elements[1].endswith(":138A")) or elements[1].endswith(":8F3A")) and (elements[3]=="01")):
               airplay_active = True
               break
      self.airplay_active = airplay_active
      return self.airplay_active
   
   def setOnActivate(self,callback):
      if callback == None:
         self.__onActivate = None
      else:
         self.__onActivate = callback
         
   def setOnDeactivate(self,callback):
      if callback == None:
         self.__onDeactivate = None
      else:
         self.__onDeactivate = callback
         
   def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
      Thread.__init__(self, group, target, name, args, kwargs) # super call
      self.airplay_active = False
      self.__onActivate = None
      self.__onDeactivate = None
      self._isStopped = False
   
   def run(self):
      # check for airplay transmissions:
      while not self._isStopped:
         sleep(AIRPLAY_POLLING_PERIOD)
         airplay_active_before = self.airplay_active
         if self.is_airplay_active() != airplay_active_before:
                if self.airplay_active:
                   if self.__onActivate != None:
                      self.__onActivate()
                else:
                   if self.__onDeactivate != None:
                      self.__onDeactivate()
   def stop(self):
      self._isStopped = True


# To use (example):
def airplay_activated():    
   print("Airplay activated")
   
def airplay_deactivated():
   print("Airplay deactivated")
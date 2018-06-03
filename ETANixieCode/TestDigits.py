#!/usr/bin/python

from locations import dest,orig
from googlemapsclientkey import clientkey
import NixieTube

import googlemaps
import datetime 
import math

import time
from time import sleep
from threading import Timer

# this timer will sychronize to system time time.time().   Great for clocks
class RepeatedSyncTimer(object):
  def __init__(self, interval ,function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.error = 0.0
    # set this so that the interval is at 50% 0f a second, for clock to update
    # only needed if we have seconds
    self.next_call = math.ceil(time.time()) + 0.5
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args,**self.kwargs)

  def start(self):
    if not self.is_running:
      #syncronize the interval to 50% to allow to account for errors in the timer.
      #the timer interval is adjusted to sychronize with real time.  
      # this is important for clocks.  Above this was set at 50% of the interval
      self.next_call += self.interval
      self._timer = Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

# in this algorithm.  print the time first, followed by each of the destinations 
# in the Array in order.


def PrtNixieDigits(timestr):
    global ind
    
    time_digits= [ind,ind,ind,ind,ind,ind]
    # test is we have twenty four hour time
    
    if ind > 9:
       ind = 0
    if ind == 9:
       z = ind
       #DigitSec.Write_Fade_Out()
       time.sleep(.05)
       for y in range (0,10):
          z+=1
          if z > 9:
             z = 0
          DigitSec.Write_Display([z,z,z,z,z,z])
          time.sleep(.0075)
       DigitSec.Display_Off() 
    else:
       if ind == 0:
          DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
       else:
          DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
       print(str(ind), time_digits)
    ind += 1



# global timer
ind = 0
# timer/ clock update rate in seconds
LoopRate = 3.0

DigitSec = NixieTube.NixieTube('IN-4',6)
#DigitSec.Pir_Sensor_On()
pre_time_digits = [0,0,0,0,0,0]
      
# start the timer circuit (first parameter is the interval in seconds)
# this circuit will then print the time to the screen and loops through the times 
# this clock will print every second
# testing nixie tubes
rt = RepeatedSyncTimer(LoopRate,PrtNixieDigits,datetime.datetime.now())


print("after timer thread call")

while True:
   # update the traffic every 4 minutes (see the sleep command)
   #testinput = raw_input("Do you want to stop: Y or Yes")
   #if testinput == 'Y' or testinput == 'Yes':
   #   break
   # update the trafic every 4 minutes usage to stay under free usage limit 
   sleep(40)
   #break
   

rt.stop()
DigitSec.Power_Off()

# algorithm for the clock


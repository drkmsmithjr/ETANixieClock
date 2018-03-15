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
    self.function(*self.args, **self.kwargs)

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

def PrtTime(timestr):
    global ind
    global TravelDuration
    global dest
    global TravelDurText
    # transtime determine how long in seconds to display the current ETA or Current time.  
    transtime = 5
    now = datetime.datetime.now()
    seconds = int(now.strftime("%S"))
    seconds = seconds % 10
    DigitSec.Write_Display([seconds])
    #print(seconds)
    # use the mod command to loop through all the destinations and print one at a time. 
    # we can use other functions and sequences to follow different activities.  
    ind2 = int(math.floor(ind/transtime))
    if ind2 >= len(dest):
       print(str(now)+ " " +  "The Current Time " + str(now))
       ind += 1
       if ind2 > len(dest):
          ind = 0
    else:
       ETA = now + datetime.timedelta(seconds=TravelDuration[ind2]) + datetime.timedelta(minutes=ETDdelay)
       print(str(now) + " "+ dest[ind2]['toplace'] + " " + str(ETA) + " Travel Time: " + TravelDurText[ind2])
       ind += 1

def PrtCurrentTimeOneNixie(timestr):
    global ind
    global TravelDuration
    global dest
    global TravelDurText
    # transtime determine how long in seconds to display the current ETA or Current time.  
    now = datetime.datetime.now()
    seconds_1digit = int(now.strftime("%S"))
    seconds_1digit = seconds_1digit % 10
    #DigitSec.Write_Display([seconds_1digit])
    Hour = int(now.strftime("%I"))
    Hour_1digit = int(math.floor(Hour/10.0))
    Hour_2digit = Hour % 10  
    Minute = int(now.strftime("%M"))
    Minute_1digit = int(math.floor(Minute/10.0))
    Minute_2digit = Minute % 10
    time_digits= [Hour_1digit,Hour_2digit,Minute_1digit,Minute_2digit]
    if ind > 4:
       ind = 0
    if ind == 4:
       z = time_digits[3]
       DigitSec.Write_Fade_Out()
       time.sleep(.05)
       for y in range (0,10):
          z+=1
          if z > 9:
             z = 0
          DigitSec.Write_Display([z])
          time.sleep(.01)
       DigitSec.Display_Off() 
    else:
       #DigitSec.Display_Off()
       #time.sleep(0.02)
       #DigitSec.Ramp_Display([time_digits[ind]])
       #DigitSec.Write_Display([time_digits[ind]])
       if ind == 0:
          DigitSec.Write_Fade_In([time_digits[ind]])
       else:
          DigitSec.Write_Fade_Out_Fade_In([time_digits[ind]])
       print(str(now), time_digits, time_digits[ind])
    ind += 1

def PrtWorkTimeOneNixie(timestr):
    global ind
    global TravelDuration
    global dest
    global TravelDurText
    # transtime determine how long in seconds to display the current ETA or Current time.  
    now = datetime.datetime.now()
    now = now + datetime.timedelta(seconds=TravelDuration[0]) + datetime.timedelta(minutes=ETDdelay)
    seconds_1digit = int(now.strftime("%S"))
    seconds_1digit = seconds_1digit % 10
    #DigitSec.Write_Display([seconds_1digit])
    Hour = int(now.strftime("%I"))
    Hour_1digit = int(math.floor(Hour/10.0))
    Hour_2digit = Hour % 10  
    Minute = int(now.strftime("%M"))
    Minute_1digit = int(math.floor(Minute/10.0))
    Minute_2digit = Minute % 10
    time_digits= [Hour_1digit,Hour_2digit,Minute_1digit,Minute_2digit]
    if ind > 4:
       ind = 0
    if ind == 4:
       z = time_digits[3]
       for y in range (0,16):
          z+=1
          if z > 9:
             z = 0
          DigitSec.Write_Display([z])
          time.sleep(.02)
       DigitSec.Display_Off() 
    else:
       #DigitSec.Display_Off()
       #time.sleep(0.02)
       #DigitSec.Ramp_Display([time_digits[ind]])
       DigitSec.Write_Display([time_digits[ind]])
       #DigitSec.Write_Fate_In([time_digits[ind]])
       print(str(now), time_digits, time_digits[ind])
    ind += 1



#global parameters for interupt.  Needs to be as larger as dest array below
TravelDuration = [0,0]
TravelDurText = [0,0]

# global timer
ind = 0
# timer/ clock update rate in seconds
LoopRate = 1.0

# how long to get actually leave (in minutes)
ETDdelay = 2 
DigitSec = NixieTube.NixieTube()
DigitSec.Pir_Sensor_On()

      
#create the google maps object using the key
gmaps = googlemaps.Client(key=clientkey)

# start the timer circuit (first parameter is the interval in seconds)
# this circuit will then print the time to the screen and loops through the times 
# 
# this clock will print every second
#rt = RepeatedSyncTimer(LoopRate,PrtTime,datetime.datetime.now())

rt = RepeatedSyncTimer(LoopRate,PrtCurrentTimeOneNixie,datetime.datetime.now())

#rt = RepeatedSyncTimer(LoopRate,PrtWorkTimeOneNixie,datetime.datetime.now())


# get the direction results for each destination.  The return is a dict object

print("after timer thread call")

while True:
   # update the traffic every 4 minutes (see the sleep command)
   for x in range (0,len(dest)):
      now = datetime.datetime.now()
      directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", avoid="tolls", departure_time = now, traffic_model = "best_guess" )
      #directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", departure_time = now, traffic_model = "best_guess" )
      TravelDuration[x] = directions_result[0]['legs'][0]['duration']['value']
      TravelDurText[x] = directions_result[0]['legs'][0]['duration']['text']
      #ETA = now + datetime.timedelta(seconds=TravelDuration[x])
      #print(dest[x]['toplace'] + " " + str(ETA) + " Duration: " + TravelDurText[x])
   # update the trafic every 4 minutes
   sleep(240)

# algorithm for the clock


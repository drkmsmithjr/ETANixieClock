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
    # test is we have twenty four hour time
    
    if ind > 4:
       ind = 0
    if ind == 4:
       z = time_digits[3]
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
       #DigitSec.Display_Off()
       #time.sleep(0.02)
       #DigitSec.Ramp_Display([time_digits[ind]])
       #DigitSec.Write_Display([time_digits[ind]])
       if ind == 0:
          #DigitSec.Write_Fade_In([time_digits[ind],time_digits[ind]])
          DigitSec.Write_Display([time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind]])
       else:
          #DigitSec.Write_Fade_Out_Fade_In([time_digits[ind],time_digits[ind]])
          DigitSec.Write_Display([time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind],time_digits[ind]])
       print(str(now), time_digits, time_digits[ind])
    ind += 1

def PrtCurrentTimeSixNixie(timestr):
    global ind
    global TravelDuration
    global dest
    global TravelDurText
    global pre_time_digits

    # how many time to display current time before spin
    time_series = 5
    # after displaying time, provide a spin
    # then display all the locations for this amount of time each (in seconds)
    location_series = 4
    # flow description
    # 1. first time_series seconds, display the time
    # 2. spin display at end of time
    # 3. present each location for location_series seconds (location number, blank, four digits)
    # 3.5 spin at each change of location.   
    # 4. repeat at 1
 
    # transtime determine how long in seconds to display the current ETA or Current time.  
    now = datetime.datetime.now()
    # test to determine if we should be using a ETA
    #print("ind")
    #print(ind)
    if ind-time_series > 0: 
       ind3 = math.floor((ind-time_series) / location_series/1.0)
       ind3 = int(ind3)
       #print("ind3")
       if ind3 >= len(TravelDuration):
          ind3 = len(TravelDuration)-1
       #print(ind3)
       now = now + datetime.timedelta(seconds=TravelDuration[ind3]) + datetime.timedelta(minutes=ETDdelay)

    seconds = int(now.strftime("%S"))
    seconds_1digit = int(math.floor(seconds/10.0))
    seconds_2digit = seconds % 10
    #DigitSec.Write_Display([seconds_1digit])
    Hour = int(now.strftime("%I"))
    Hour_1digit = int(math.floor(Hour/10.0))
    Hour_2digit = Hour % 10  
    Minute = int(now.strftime("%M"))
    Minute_1digit = int(math.floor(Minute/10.0))
    Minute_2digit = Minute % 10
    if ind-time_series <=  0:
       time_digits= [Hour_1digit,Hour_2digit,Minute_1digit,Minute_2digit,seconds_1digit,seconds_2digit]
       if Hour_1digit == 1:
          BlankCntrl = []
       else:
          BlankCntrl = [False,True,True,True,True,True]
          #BlankCntrl = [True,True,True,True,True,True] 
    else:
       time_digits = [ind3+1,0,Hour_1digit,Hour_2digit,Minute_1digit, Minute_2digit]
       if Hour_1digit == 1:
          BlankCntrl = [True,False,True,True,True,True]
       else:
          BlankCntrl = [True,False,False,True,True,True]
          
    if ind > time_series + location_series*len(TravelDuration):
       ind = 0
    # spin at end of displaying time or at the end of each location_series display
    if (ind == time_series) or (ind-time_series>0 and ((ind-time_series)%location_series == 0)):
       z = pre_time_digits
       #DigitSec.Write_Fade_Out()
       time.sleep(.05)
       for y in range (0,10):
          #increment z
          for g in range (0,len(z)):
             z[g] += 1   
             if z[g] > 9:
                z[g] = 0
          DigitSec.Write_Display(z,BlankCntrl)
          time.sleep(.002)
       DigitSec.Display_Off() 
    else:
       #DigitSec.Display_Off()
       #time.sleep(0.02)
       #DigitSec.Ramp_Display([time_digits[ind]])
       #DigitSec.Write_Display([time_digits[ind]])
       #blink the seconds
       #BlkCntrl2 = BlankCntrl
       if ind-time_series <=  0:
          #BlankCntrl2 = BlankCntrl
          #BlkCntrl2[4]=False
          #BlkCntrl2[5]=False
          if Hour_1digit == 1:
             DigitSec.Write_Display(time_digits,[True,True,True,True,False,False])
          else:
             DigitSec.Write_Display(time_digits,[False,True,True,True,False,False])
          time.sleep(.05)
       if ind == 0:
          #DigitSec.Write_Fade_In([time_digits[ind],time_digits[ind]])
          DigitSec.Write_Display(time_digits,BlankCntrl)
       else:
          #DigitSec.Write_Fade_Out_Fade_In([time_digits[ind],time_digits[ind]])
          DigitSec.Write_Display(time_digits,BlankCntrl)
       print(str(now), time_digits)
    ind += 1
    if ind > time_series + location_series*len(TravelDuration):
       ind = 0
    pre_time_digits = time_digits

def updateETA():

     for x in range (0,len(dest)):
      now = datetime.datetime.now()
      print(str(now))
      try:
         directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", avoid="tolls", departure_time = now, traffic_model = "best_guess" )
      #directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", departure_time = now, traffic_model = "best_guess" )
         TravelDuration[x] = directions_result[0]['legs'][0]['duration']['value']
         TravelDurText[x] = directions_result[0]['legs'][0]['duration']['text']
      #ETA = now + datetime.timedelta(seconds=TravelDuration[x])
         print(dest[x]['toplace'] + " " + " Duration: " + TravelDurText[x])
      except:
         print("There was a fault in the directions_result. restablishing connection")
         gmaps = googlemaps.Client(key=clientkey)
         directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", avoid="tolls", departure_time = now, traffic_model = "best_guess" )
         #directions_result = gmaps.directions(origin=orig,destination = dest[x]['toaddress'], mode = "driving", departure_time = now, traffic_model = "best_guess" )
         TravelDuration[x] = directions_result[0]['legs'][0]['duration']['value']
         TravelDurText[x] = directions_result[0]['legs'][0]['duration']['text']  
         print(dest[x]['toplace'] + " " + " Duration: " + TravelDurText[x])

#global parameters for interupt.  Needs to be as larger as dest array below
TravelDuration = [0]*len(dest)
TravelDurText = [0]*len(dest)

# global timer
ind = 0
# timer/ clock update rate in seconds
LoopRate = 1.0

# how long to get actually leave (in minutes)
ETDdelay = 2 
DigitSec = NixieTube.NixieTube('IN-4',6)
#DigitSec.Pir_Sensor_On()
pre_time_digits = [0,0,0,0,0,0]
      
#create the google maps object using the key
gmaps = googlemaps.Client(key=clientkey)
#sleep(10)

# start the timer circuit (first parameter is the interval in seconds)
# this circuit will then print the time to the screen and loops through the times 
# 
# this clock will print every second
# testing nixie tubes
rt = RepeatedSyncTimer(LoopRate,PrtCurrentTimeOneNixie,datetime.datetime.now())
# the ETANixieClock routine
#rt = RepeatedSyncTimer(LoopRate,PrtCurrentTimeSixNixie, datetime.datetime.now())

#sleep(5)

# start the updateETA routine
updateETATime = 240
# run to initially get ETA
updateETA()
# start time
timerETA = RepeatedSyncTimer(updateETATime,updateETA)
# get the direction results for each destination.  The return is a dict object

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
timerETA.stop()
DigitSec.Power_Off()

# algorithm for the clock


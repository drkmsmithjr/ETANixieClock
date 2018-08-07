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
      # test to see if next call if negative.  if so,then set for 0.1 second
      if (self.next_call - time.time()) < 0:
         self.next_call = time.time() + 0.1
      self._timer = Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

# in this algorithm.  print the time first, followed by each of the destinations 
# in the Array in order.


def PrtNixieDigits(timestr, burntime):
    global ind
    
    time_digits= [ind,ind,ind,ind,ind,ind]
    # test is we have twenty four hour time
    
    DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
    print("Digit " + str(ind)+" is being driven now")
    print("the timer is set for %s minutes" % (burntime/60))
    ind += 1
    if ind > 9:
       ind = 0

def PrtEvenOddNixieDigits(timestr, burntime):
    global ind
    
    time_digits= [ind,ind,ind,ind,ind,ind]
    # test is we have twenty four hour time
        
    DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
    print("Digit " + str(ind)+" is being driven now")
    print("the timer is set for %s minutes" % (burntime/60))
    ind += 2
    if ind > 9:
       ind = 0

def CheckTimer (rt2):
    global ind
    
    print("The Burn in is now done")
    rt2.stop()
    DigitSec.Power_Off()
    

def PrtOddNixieDigits(timestr):
    global ind
    
    time_digits= [ind,ind,ind,ind,ind,ind]
    # test is we have twenty four hour time
        
    DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
    print(str(ind), time_digits)
    ind += 2
    if ind > 9:
       ind = 0



# global timer
ind = 0
# Second timer
SecondTimer = False

# timer/ clock update rate in seconds
LoopRate = 2.0

DigitSec = NixieTube.NixieTube('IN-4',6)
#DigitSec.Pir_Sensor_On()
pre_time_digits = [0,0,0,0,0,0]
      
# start the timer circuit (first parameter is the interval in seconds)
# this circuit will then print the time to the screen and loops through the times 
# this clock will print every second
# testing nixie tubes
rt = RepeatedSyncTimer(LoopRate,PrtNixieDigits,datetime.datetime.now(), LoopRate)


print("after timer thread call")

while True:
   # update the traffic every 4 minutes (see the sleep command)
   #testinput = raw_input("Do you want to stop: Y or Yes")
   #if testinput == 'Y' or testinput == 'Yes':
   #   break
   # update the trafic every 4 minutes usage to stay under free usage limit 
   #sleep(40)
   raw_option = raw_input("")
   rt.stop()
   if SecondTimer:
      rt2.stop()
      Stoptimer.stop()
   if raw_option == "t":
      rt.start()
      print ("Timer started")
   elif raw_option == "T":
      while True:
         raw_option2 = raw_input("Enter the number of minutes for All digits:")
         if raw_option2.isdigit():
            # we will start time by writting a zero, timer will update from 1,2,3,4...9
            ind = 0
            DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
            ind = 1
            burntime = int(raw_option2)
            burntime = burntime*60
            print("Digit 0 is being driven now")
            print("the timer is set for %s minutes" % (burntime/60))
            rt2 = RepeatedSyncTimer(burntime,PrtNixieDigits,datetime.datetime.now(),burntime)
            Stoptimer = RepeatedSyncTimer((burntime*10-5),CheckTimer,rt2)
            SecondTimer = True
            break
         else:
            print("Please try again: need to input a digit")
   elif raw_option == "ET":
      while True:
         raw_option2 = raw_input("Enter the number of minutes for each Even digit:")
         if raw_option2.isdigit():
            # we will start time by writting a zero, timer will update from 2,4,6,8
            ind = 0
            DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
            ind = 2
            burntime = int(raw_option2)
            burntime = burntime*60
            print("Digit 0 is being driven now")
            print("the timer is set for %s minutes" % (burntime/60))
            rt2 = RepeatedSyncTimer(burntime,PrtEvenOddNixieDigits,datetime.datetime.now(),burntime)
            Stoptimer = RepeatedSyncTimer((burntime*5-5),CheckTimer,rt2)
            SecondTimer = True
            break
         else:
            print("Please try again: need to input a digit")
   elif raw_option == "OT":
      while True:
         raw_option2 = raw_input("Enter the number of minutes for each Odd digit:")
         if raw_option2.isdigit():
            # we will start time by writting a zero, timer will update from 2,4,6,8
            ind = 1
            DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
            ind = 3
            burntime = int(raw_option2)
            burntime = burntime*60
            print("Digit 1 is being driven now")
            print("the timer is set for %s minutes" % (burntime/60))
            rt2 = RepeatedSyncTimer(burntime,PrtEvenOddNixieDigits,datetime.datetime.now(),burntime)
            Stoptimer = RepeatedSyncTimer((burntime*5-5),CheckTimer,rt2)
            SecondTimer = True
            break
         else:
            print("Please try again: need to input a digit")   
   elif raw_option == "dT":
      while True:
         raw_option3 = raw_input("Enter the digit to Test ")
         raw_option2 = raw_input("Enter the number of minutes for digit:")
         if raw_option2.isdigit() and raw_option3.isdigit():
            # we will start time by writting a zero, timer will update from 2,4,6,8
            ind = int(raw_option3)
            DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
            burntime = int(raw_option2)
            burntime = burntime*60
            print("Digit %s is being driven now" % ind)
            print("the timer is set for %s minutes" % (burntime/60))
            rt2 = RepeatedSyncTimer(burntime,PrtEvenOddNixieDigits,datetime.datetime.now(),burntime)
            Stoptimer = RepeatedSyncTimer((burntime*1-5),CheckTimer,rt2)
            SecondTimer = True
            break
         else:
            print("Please try again: need to input digits")      
   elif len(raw_option) == 0:
      ind += 1
      if ind > 9:
         ind = 0
      DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
      print ("indexed digit to next one: %s" % ind)   
   elif raw_option == "x":
      break
   # turn off N_DISABLE 
   elif raw_option == "d":
      if DigitSec.DISPLAY_ON:
         DigitSec.Display_Off()
         print("display off")
      else:
         DigitSec.Display_On()
         print("display on")
   elif raw_option == "p":
      if DigitSec.POWER_ON:
         DigitSec.Power_Off()
         print("power Off")
      else:
         DigitSec.Power_On()
         print("power_on")
   elif len(raw_option) == 1:
      if raw_option.isdigit():
         ind = int(raw_option)
         DigitSec.Write_Display([ind,ind,ind,ind,ind,ind])
         print(" output a: %s" % ind)
      else:
         print ("the wrong option was chosen")
   else:
      print("The choice was not valid, please try again")
   print ("\r\r\r")
   
      
         
   print("press:")
   print("return: to index the displayed diget to the next value")
   print("[t]: to start time 1-9:")
   print("[T]: For a x minute burn in of all digits")
   print("[0-9]: to display the digit to light up")
   print("[d]: to toggle display N_DISABLE")
   print("[p]: to toggle the power supply on/off")
   print("[OT]: for a x minute burn in of odd digits (for biquaniary driven tubes")
   print("[ET]: for a x minute burn in of even digits (for biquinary driven tubes)")
   print("[x]: to exit program")
     
   
   #break
   

rt.stop()
DigitSec.Power_Off()

# algorithm for the clock


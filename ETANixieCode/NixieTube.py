#!/usr/bin/python
import RPi.GPIO as GPIO
import math
import time
import threading

# the tubes are architected to be a serial bit stream input.  
# the nixie type is for different types of Nixies

# BCM GPIP pin numbers being used 
N_DATA = 17
DATA_CLK = 27
LOAD = 22
N_DISABLE = 10
N_SR_CLR = 9
N_EN_PowerSupply = 5
PIR_SENSE=4


class NixieTube():

   def __init__(self,nixietype = 'IN-4', elements = 1 , PIR_SENSOR = False):
        self.nixietype = nixietype
        self.elements = elements
        # the displayed Digits to keep track of current state.  Initially empty
        # digits and StoredDigits will be a array of integers representing the digits to be displayed
        

        self.StoredDigits = []
        # the data that will be transferred to update the display
        self.SerialData = []
        for x in range (0,self.elements):
           self.StoredDigits.append(0)
        #setup GPIO to use the BCM numbering.  The adufruit extension shows the BCM 
        # BCM numbering
        GPIO.setmode(GPIO.BCM)   
        # set warnings false to avoid generating errors when the channel was set already
        GPIO.setwarnings(False)
        # intially set N_data high so data is low    
        GPIO.setup(N_DATA,GPIO.OUT, initial=GPIO.HIGH)
        # Data gets shifted in on the falling edge of DATA_CLK
        GPIO.setup(DATA_CLK,GPIO.OUT, initial=GPIO.LOW)
        # The LOAD will transfer shift registers to storge registers on falling edge of LOAD
        GPIO.setup(LOAD,GPIO.OUT , initial=GPIO.LOW)
        # NDISABLE: keeping this low will keep all outputs off on IC 
        self.DISPLAY_ON = False
        GPIO.setup(N_DISABLE,GPIO.OUT , initial=GPIO.LOW)
        # When Low shift registers are transferred to storage registers
        GPIO.setup(N_SR_CLR,GPIO.OUT , initial=GPIO.LOW)
        self.register_clear()
        # pulling low will ENABLE power supply
        self.POWER_ON = False
        GPIO.setup(N_EN_PowerSupply,GPIO.OUT , initial=GPIO.HIGH)
        # set the PIR_SENSE to an input and if the NixieTube has PIR_SENSOR..
        # PIR_SENSOR can also be used to turn on/off the PIR_SENSOR operation
        # Default of PIR_SENSOR is False
        # Default of the PIR_SENSE = True... ensure the clock will turn on
        self.PIR_SENSOR = PIR_SENSOR
        #self.PIR_SENSOR = True
        self.PIR_SENSE = True
        # PIR delay is in minutes
        self.PirDelay = 1
        GPIO.setup(PIR_SENSE,GPIO.IN)
        # define the sampling rate and delays for the PIR sensor in seconds 
        # the PIR sensor has a delay of 4 seconds.  so every 3 seconds will ensure to capture event
        self.PirSampling = 1
        self.CurrentDelay = 0
        # start the thread to sample the PIR Sensor
        self.PirSampleThread = threading.Thread(target = self.PirSample, args = (self.PirSampling,self.PirDelay))
        self.PirSampleThread.daemon = True 
        self.PirSampleThread.start()
              

   def PirSample(self,PirSampling,PirDelay):
        # this routine will run in a thread
        # if the PIR_SENSOR is On/ACTIVE, it will test the input
        # it will sample the PIR sensor every PirSampling rate
        # and it will update the PIR_SENSE boolean solution
        next_call = time.time()
        while self.PIR_SENSOR:
           #test PIR_SENSE input.
           self.CurrentDelay += PirSampling
           #print(self.CurrentDelay)
           if GPIO.input(PIR_SENSE):
              self.CurrentDelay = 0
           if self.CurrentDelay > (PirDelay*60):
              self.PIR_SENSE = False
              self.Power_Off()
              #clamp the currentDelay to max value
              self.CurrentDelay = PirDelay*60+1
           else:
              self.PIR_SENSE = True
           print(self.PIR_SENSE,self.CurrentDelay,GPIO.input(PIR_SENSE))
           next_call = next_call + PirSampling
           time.sleep(next_call - time.time())
                
   def digitsToSerial (self,digits,BlankCntrl = []):
        # this routine will conver the digits into the correct serial string.       
        # digits is an array that has at least # elemnts in it.
        # each digit will be converted into 6 serial bits.
        # bit 6 is even or odd (1 for even, 0 for odd)
        # the other 5 bits are zero except for the displayed digits
        # (ODD/EVEN BIT, 0-1,2-3,4-5,6-7, MSB = 8-9)
        # BlankCntrl is an optional parameter
        # that allows easy blanking of one digit in string
        # It will be an array of Booleans that correspond to the digits array
        # True for display, False for Blanking of that digit (not display)
        # for 12h time, the first digit is often not displayed.
        # test is BlankCntrl is empty, then default to display all 
        if len(BlankCntrl) == 0:
           for x in range (0, self.elements):
              BlankCntrl.append(True)       
        #Resetting serial data
        self.SerialData = []
        for x in range (0,self.elements):
           # find the digit numbering
           dignum = math.floor(digits[x]/2.0)
           # convert this into a power of two + 1  
           sdata = int(2**(dignum+1))
           # test to see if we should blank this displayed.  TRUE mean display digit 
           if BlankCntrl[x] == True:
              # bit wise OR with bin(64) or 7 sigit binary so we can perform bitwise ops
              sdata = sdata | 0b1000000
           else:
              #ensure all data is zero bits,2,3,4,5,6.   7th bit will be still even or odd and set.    
              sdata = 0b1000000
           # test for EVEN or ODD.  If EVEN, then LSB = 1
           if digits[x] % 2.0 == 0:
              sdata = sdata | 0b1
           # perform an exclusive or to get NDATA
           sdata = sdata ^ 0b111111
           strdata = bin(sdata)
           # now put the binary into array of 0 or 1 integers.  Ignore first 3 characters
           # these characters will be 0b1 from above
           for x in range (3,9):
              self.SerialData.append(int(strdata[x]))
        #print(self.SerialData)
        
   def ShiftData(self):
     # this will shift the SerialData into the serial registers
     # the data is loaded, then the data_clk goes high then low to clock in 
        for x in self.SerialData:
           GPIO.output(N_DATA, x)
           self.data_clock()
        GPIO.output(N_DATA,GPIO.HIGH)   
           
   def data_clock(self):
        GPIO.output(DATA_CLK,GPIO.HIGH)
        time.sleep(.001)         
        GPIO.output(DATA_CLK,GPIO.LOW)
        
   def LoadData(self):
        GPIO.output(LOAD,GPIO.HIGH)
        time.sleep(.001)         
        GPIO.output(LOAD,GPIO.LOW)  
        
   def register_clear(self):
        GPIO.output(N_SR_CLR,GPIO.HIGH)
        time.sleep(.001)         
        GPIO.output(N_SR_CLR,GPIO.LOW)
        
   def Display_On(self):
        if self.DISPLAY_ON == False:
           GPIO.output(N_DISABLE,GPIO.HIGH)
           self.DISPLAY_ON = True
   
   def Display_Off(self):
        if self.DISPLAY_ON:
           GPIO.output(N_DISABLE,GPIO.LOW)
           self.DISPLAY_ON = False
           time.sleep(.001)     

   def Power_On(self):
        if self.POWER_ON == False and self.PIR_SENSE:
        #if self.POWER_ON == False:
           GPIO.output(N_EN_PowerSupply,GPIO.LOW)
           self.POWER_ON = True 
           time.sleep(0.100)    

   def Power_On_Nodelay(self):
        if self.POWER_ON == False and self.PIR_SENSE:
        #if self.POWER_ON == False:
           GPIO.output(N_EN_PowerSupply,GPIO.LOW)
           self.POWER_ON = True 
           time.sleep(0.100)     
           
   def Power_Off(self):
        if self.POWER_ON:
           GPIO.output(N_EN_PowerSupply,GPIO.HIGH)
           self.POWER_ON = False
           time.sleep(.001)     

   def Write_Display(self, digits, BlankCntrl = []):
        self.Power_On()
        self.digitsToSerial(digits, BlankCntrl)
        self.register_clear()
        self.ShiftData()
        self.Display_Off()
        self.LoadData()
        self.Display_On()

   def Write_Display_No_Off(self, digits, BlankCntrl = []):
        self.Power_On()
        self.digitsToSerial(digits, BlankCntrl)
        self.register_clear()
        self.ShiftData()
        #self.Display_Off()
        self.LoadData()
        self.Display_On()
        self.StoredDigits = digits

   def Write_Spin_Digits(self, z, BlankCntrl = [], spin = 10):
        # Will take the current digits (z) and spin them in place for 
        # spin times .
        # there is a delay=2ms between displays
        # the total time for the spin is going to be write_display * spin.   
        delay = .002
        # power on the display if it is off.   
        self.Power_On()
        for y in range (0,spin):
          #increment z and reset to zero if reach 10
          for g in range (0,len(z)):
             z[g] += 1   
             if z[g] > 9:
                z[g] = 0
          self.Write_Display(z,BlankCntrl)
          time.sleep(delay)

   def Write_Spin_To_Digits(self, orig_digits, new_digits, orig_BlankCntrl = [], new_BlankCntrl = [], startspin = 5, transpin = 3):
        # Will take the current digits (z) and spin them in place and 
        # then start to display the new digits one at a time for number of total elements
        # the startspin is number of spins before starting
        # the transpins is the spins during transitions.
        # there is a delay=2ms between displays
        # the total time for the spin is going to be write_display * spin.   
        delay = .002
        # power on the display if it is off.   
        self.Power_On()

        orig_digitsCpy = list(orig_digits)
        orig_BlankCntrlCpy = list(orig_BlankCntrl)
        ind_digits = []
        ind_BlankCntrl = []

        # we need to use blank cntrl in this routine
        if orig_BlankCntrl == []:
           orig_BlankCntrlCpy = [True]*len(orig_BlankCntrl)

        if new_BlankCntrl == []:
           new_BlankCntrl = [True]*len(new_BlankCntrl)

        
        # spin then all now 
        for y in range (0,startspin):
          #increment z and reset to zero if reach 10
          for g in range (0,len(orig_digitsCpy)):
             orig_digitsCpy[g] += 1   
             if orig_digitsCpy[g] > 9:
                orig_digitsCpy[g] = 0
          self.Write_Display(orig_digitsCpy,orig_BlankCntrlCpy)
          time.sleep(delay)

        # now fix the first new digit and spin the rest of them
        for y in range(0,len(new_digits)):
          # add one to ind_digits
          # pop one from top of orig_digits
          ind_digits.append(new_digits[y])
          ind_BlankCntrl.append(new_BlankCntrl[y])
          orig_digitsCpy.pop(0)
          orig_BlankCntrlCpy.pop(0)
          # spin just the original digits fixing the rest
          for x in range (0,transpin):
          #increment z and reset to zero if reach 10
             for g in range (0,len(orig_digitsCpy)):
                orig_digitsCpy[g] += 1   
                if orig_digitsCpy[g] > 9:
                   orig_digitsCpy[g] = 0
             self.Write_Display(ind_digits+orig_digitsCpy,ind_BlankCntrl+orig_BlankCntrlCpy)
             time.sleep(delay)

          # update the ind_digits with the new BlankCntrl
          # now spin the original digits


   def Write_Fade_Out_Fade_In(self, digits, BlankCntrl = []):
        #print("digits into functions")
        #print(digits)
        self.Power_On()
        Tperiod = .0075   
        Cycles = 30
        #print(self.StoredDigits)
        #Fade OUt
        for x in range (0,Cycles):
           self.Display_On()
           time.sleep(Tperiod*(Cycles-x-1)/Cycles)
           self.digitsToSerial(self.StoredDigits, BlankCntrl)
           self.register_clear()
           self.ShiftData()
           self.LoadData()
           self.Display_Off()
           time.sleep(Tperiod*(x+1)/Cycles)
        #Fade In
        Cycles = 20
        for x in range (0,Cycles):
           self.Display_Off() 
           time.sleep(Tperiod*(Cycles-x-1)/Cycles)
           self.digitsToSerial(digits,BlankCntrl)
           self.register_clear()
           self.ShiftData()
           self.LoadData()
           self.Display_On()
           time.sleep(Tperiod*(x+1)/Cycles)
        self.digitsToSerial(digits, BlankCntrl)
        self.register_clear()
        self.ShiftData()
        self.LoadData()
        self.Display_On()
        self.StoredDigits = digits
        #print("stored digits")
        #print(digits)

   def Write_Fade_Out(self):
        # Fade_Out will take the StoredDigits and Fade it out.
        # Tperiod is the Period of on and off
        # cycles is how many cycles to make up the period.   
        # Tperiod*Cycles is the total transition time 
        self.Power_On()
        Tperiod = .0075   
        Cycles = 30
        print(self.StoredDigits)
        #Fade OUt
        for x in range (0,Cycles):
           self.Display_On()
           time.sleep(Tperiod*(Cycles-x-1)/Cycles)
           self.digitsToSerial(self.StoredDigits, BlankCntrl)
           self.register_clear()
           self.ShiftData()
           self.LoadData()
           self.Display_Off()
           time.sleep(Tperiod*(x+1)/Cycles)

   def Write_Fade_In(self, digits, BlankCntrl = []):
        # Fade_Out will take the StoredDigits and Fade it out.
        # Tperiod is the Period of on and off
        # cycles is how many cycles to make up the period.   
        # Tperiod*Cycles is the total transition time
        self.Power_On()
        Tperiod = .0075   
        Cycles = 20
        print(self.StoredDigits)
        #Fade OUt
        
        #Fade In
        for x in range (0,Cycles):
           self.Display_Off() 
           time.sleep(Tperiod*(Cycles-x-1)/Cycles)
           self.digitsToSerial(digits, BlankCntrl)
           self.register_clear()
           self.ShiftData()
           self.LoadData()
           self.Display_On()
           time.sleep(Tperiod*(x+1)/Cycles)
        self.digitsToSerial(digits, BlankCntrl)
        self.register_clear()
        self.ShiftData()
        self.LoadData()
        self.Display_On()
        self.StoredDigits = digits

   def Write_In_Fade_Out(self, digits, BlankCntrl = []):
        # Fade_Out will take the StoredDigits and Fade it out.
        # Tperiod is the Period of on and off
        # cycles is how many cycles to make up the period.   
        # Tperiod*Cycles1 + Tperiod*Cycles2 is the total transition time 
        self.Power_On()
        Tperiod = .0010   
        Cycles = 20
        print(self.StoredDigits)
        for x in range (0,Cycles):
           self.digitsToSerial(digits, BlankCntrl)
           self.register_clear()
           self.ShiftData()
           self.LoadData()
           self.Display_On()
           time.sleep(Tperiod*(x+1)/Cycles)
           self.digitsToSerial(self.StoredDigits,BlankCntrl)
           self.register_clear()
           self.ShiftData()
           self.LoadData()
           self.Display_On()
           time.sleep(Tperiod*(Cycles - x-1)/Cycles)
        self.digitsToSerial(digits, BlankCntrl)
        self.register_clear()
        self.ShiftData()
        self.LoadData()
        self.Display_On()
        self.StoredDigits = digits


   def Ramp_Display(self,digits, BlankCntrl = []):
   # turn on the nixie tube while ramping supply
        self.Power_Off()
        time.sleep(.125)
        self.digitsToSerial(digits, BlankCntrl)
        self.register_clear()
        self.ShiftData()
        self.Display_Off()
        self.LoadData()
        self.Display_On()
        for x in range(0,10):
           self.Power_On_Nodelay()
           time.sleep(.02)
           self.Power_Off
           time.sleep(.01)
        self.Power_On_Nodelay()
        time.sleep(.05)
        self.StoredDigits = digits
        
   def Pir_Sensor_On(self):
        self.PIR_SENSOR = True    
   
   def Pir_Sensor_Off(self):
        self.PIR_SENSOR = False

   def Pir_Delay_set(self,minutes):
        self.PirDelay = minutes    

  
if __name__ == "__main__":
        print "hello world"
       
        x = NixieTube()
        #x.Power_On()
        #for y in range (0,10):
        #   x.digitsToSerial([y])
        #   print(y,x.SerialData)
        #   x.ShiftData()
        #for y in range (0,10):
        #   x.data_clock()
        #for y in range (0,10):
        #   x.LoadData()
        #for y in range (0,10):
        #   x.register_clear()
        #for y in range (0,10):
        #   x.Display_On()
        #   x.Display_Off()
        #x.Write_Display([8])
        #time.sleep(0.5)
        #x.Write_Display([9])
        #time.sleep(0.5)       
        #x.Display_Off()
        y = 0
        z = 0

        while True:
           z += 1
           try:
              time.sleep(.02)
              x.Write_Display([y])
              y += 1
              if y > 9:
                  y = 0
              if z > 200:
                  break 
           except:
              time.sleep(0.2)
              x.Display_Off()
        x.Display_Off()
        x.Power_Off()
        

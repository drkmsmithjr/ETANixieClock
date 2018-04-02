# [Estimated Time of Arrival (ETA) Nixie Tube Clock](https://wp.me/p85ddV-B1 )
This DIY project will combine the estimated time of arrival function with a nixie tube display to create an estimated time of arrival (ETA) Nixie tube clock. It is all easily controlled by a Raspberry Pi Zero W that is connected to the internet through WiFi to provide the latest time and gets the ETA for any number of destinations. The travel time is provided by the free Google Directions API interface that includes traffic to give the best estimates on any particular day.   The goal is that with an ETA Nixie tube clock, no math is needed to add a rough, often optimistic travel time, to the actual time to determine if we are running late.   The clock does that for you and with the power of IOT, is much more accurate!    A motion sensor is also added to the clock to turn off the Nixie Tube Display when no one is around, saving power and increasing the nixie tube lifetime.    The complete project, including the six IN-4 Nixie tubes, are powered from a 1 amp iPhone charger using the 5v to 170v Nixie Tube Power supply described in another repository. 

See [www.surfncircuits.com](https://wp.me/p85ddV-B1)  for a complete description.  This github repository contains the Kicad Schematic, Spice Simulation, Efficiency Calculations of the Estimated Time of Arrival (ETA) Nixie Tube Clock.   

![PNG of the Schematic](https://github.com/drkmsmithjr/ETANixieClock/blob/master/KC-ETAclock-5v/NixieSchematic.png)

__ETANixieCode__:  This is the python code that will be placed in the ETANixieClock directory on the Raspberry Pi zero.    

__KC_ETAclock-5v__:  KiCad schematic, PCB Layout, BOM of the ETA Nixie tube clock.  You can order the PCB from oshPark at <a href="https://oshpark.com/shared_projects/B9CmGCXJ"><img src="https://oshpark.com/assets/badge-5b7ec47045b78aef6eb9d83b3bac6b1920de805e9a0c227658eac6e19a045b9c.png" alt="Order from OSH Park"></img></a>  

__SimCalcFiles__:  Spice simulation files of the Nixie Tube bi-quinary driving circuit.    

__Datasheeets__: Datasheets for the pinout and the TPIC6B595.  In the Kicad Schematic, the part numbers and Digikey (TM) links are listed already.   Also the complete BOM is located in the KC-ETAclock-5v Directory (ETAclock_BOM.ods).      

See the complete blogs entry at  [www.surfncircuits.com]()



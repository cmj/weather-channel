# Retro Winnipeg Weather Channel
# Original By probnot
# Updated/modified for USA by TechSavvvvy

from tkinter import *
import time
import datetime
import feedparser # for RSS feed
import requests # for RSS feed
import json # for RSS feed
import pygame # for background music
import random # for background music
import os # for background music
import re # for word shortener
from noaa_sdk import NOAA #Used to import data from National Weather Service, added by -TS

prog = "wpg-usa"
ver = "1.3"

#probnot's Retro Winnipeg Weather Channel USA version by TechSavvvvy
#Started on June 27, 2024, last updated July 8, 2024

#Change log
#V 1.0
       # Massive overhaul to display USA data using NOAA and US National Weather service, far too many changes to list here
       # Retained most of probnot's code, except for s1 - s8 lines (used to display text)
       # The music player has been disabled/commented out due to issues getting the original verison of this to run, hoping to bring back later
       # Increased number of lines to 1,564, from probnot's 838 lines
       #Disabled/skipped screens 3-5, 9
# 1.1
      #Removed probnot's chagelog/notes section, to make things cleaner
      #Added this section written by me (TechSavvvvy)
      #Removed all code related to env_canada
      #Removing env_canda broke the time/date display used in S1, will need to be fixed later
      #Reduced from 1,564 lines to 1,219 lines, with plans to further reduce
#1.2
     #Wrote shortFDetermine function, reducing lines of code to determine shortForcast (instead of repeating the 
            #if/elif statements 22 TIMES!!) 
     #Added statements to shortFDetermine function
     #Moved probnot's debug msg routine to top of program
     #Added debug messages to my code to show progess as data is pulled in and variables are setup
     #Reduced from 1,1219 to 972 lines.
#1.3
     #Added statements to shortFDetermine function
     #Fixed time/date on pages 1 and 6-8, which was broken after removing env_canada in version 1.1
     #Fixed music player (Wasn't broken, it was commented out in V1 for troubleshooting)
     #Increased from 972 to 1048 lines
#Fixes
     #Add way to easily turn music player on/off
     #Adjust screens 6-8 to show full city name

ZIP = 97035 #Enter USA ZIP code here, added by -TS, TX-75007 Kill Devil Hills 27948
def shortFDetermine(dirtyIn): #Used to determine forcast, called by pages 1-2, 6-8 (3-5 are currently disabled)
     if 'Mostly Clear' in dirtyIn:
        return "MOSTLY CLEAR"
     elif 'Clear' in dirtyIn:
        return "CLEAR"
     elif 'Mostly Cloudy' in dirtyIn:
        return "MOSTLY CLOUDY"
     elif 'Partly Cloudy' in dirtyIn:
        return "PARTLY CLOUDY"
     elif 'Mostly Sunny' in dirtyIn:
        return "MOSTLY SUNNY"
     elif 'Scattered Showers And Thunderstorms' in dirtyIn:
        return "STORMS/RAIN"
     elif 'Chance Showers And Thunderstorms' in dirtyIn:
        return "STORMS/RAIN"
     elif 'Sunny' in dirtyIn:
        return "SUNNY"
     elif 'Isolated Rain Showers' in dirtyIn:
        return "RAIN"
     elif 'Showers And Thunderstorms Likely' in dirtyIn:
        return "STORMS LIKELY"
     elif 'Isolated Showers And Thunderstorms' in dirtyIn:
        return "STORMS/RAIN"
     elif 'Slight Chance Showers And Thunderstorm' in dirtyIn:
        return "STORMS POSSIBLE"
     else:
        print("Unknown Forcast" + dirtyIn)
        return "ERROR"
# DEF debug messenger
def debug_msg(message, priority): #Written by probnot, moved to the top so it would work earlier

    debugmode = 1;
    # 0 = disabled
    # 1 = normal (priority 1)
    # 2 = verbose (priority 2)
    
    timestamp = 2; #Disabled because it was causing problems
    # 0 = no date/time - Why would you ever want this? Enjoy!
    # 1 = time only
    # 2 = date & time
    
    # date/time string data
    if (timestamp == 1):
        timestr = time.strftime("%H:%M.")
    elif (timestamp == 2):
        timestr = time.strftime("%Y%m%d-%H:%M.")
    else:
        timestr = ""
        
    # print debug message based on debug mode
    if ((debugmode > 0) and (priority <= debugmode)):
        print(timestr + prog + "." + ver + "." + message)
#Set current date/time
current_time = datetime.datetime.now()
if current_time.month == 1:
      Month = "JAN"
elif current_time.month == 2:
      Month = "FEB"
elif current_time.month == 3:
      Month = "MAR"
elif current_time.month == 4:
      Month = "APR"
elif current_time.month == 5:
      Month = "MAY"
elif current_time.month == 6:
      Month = "JUN"
elif current_time.month == 7:
      Month = "JUL"
elif current_time.month == 8:
      Month = "AUG"
elif current_time.month == 9:
      Month = "SEP"
elif current_time.month == 10:
      Month = "OCT"
elif current_time.month == 11:
      Month = "NOV"
elif current_time.month == 12:
      Month = "DEC"
else:
      Month = "ERR"
#Determine Hour and AM/PM
if current_time.hour >= 12:
     Hour = current_time.hour - 12
     AM_PM = "PM"
elif current_time.hour < 12:
     Hour = current_time.hour
     AM_PM = "AM"
else:
     Hour = "ER"
Hour_String = str(Hour)
#Determine Weekday
if current_time.weekday() == 0:
     Day = "MON"
elif current_time.weekday() == 1:
     Day = "TUE"
elif current_time.weekday() == 2:
     Day = "WED"
elif current_time.weekday() == 3:
     Day = "THU"
elif current_time.weekday() == 4:
     Day = "FRI"
elif current_time.weekday() == 5:
     Day = "SAT"
elif current_time.weekday() == 6:
     Day = "SUN"
else:
     Day = "ERR"
#Set Time Zone
TZ = time.tzname
TZ_String = str(TZ)
#Set current Date
Date_String = str(current_time.day)
if current_time.day < 10:
    Date = ("0" + Date_String)
else:
    Date = Date_String #This originally said current_time.day. It was retroactivley fixed to make this more reliable.
#Set current year
Year_String = str(current_time.year)
#Get current weather data from NWS
debug_msg("Getting Page 1 and 2 Weather Data",1)
n = NOAA()
res = n.get_forecasts(ZIP, 'US')
for i in res:
    curr_weaval = str(i) #Convert i to string, stored as Current_WeatherValue (curr_weaval) 
    break
#Set current temp
tempDirty = (curr_weaval[140:150])
temp = re.sub("\D", "", tempDirty)
#Set current short forcast
forcastDirty = (curr_weaval[450:560]) #Originally 450:535
shortForcast = shortFDetermine(forcastDirty)
#Set current humidity
humidDirty = (curr_weaval[355:405])
humid = re.sub("\D", "", humidDirty)
#Set current Wind Speed
WindDirDirty = (curr_weaval[420:475]) #originally 442:450
if 'SE' in WindDirDirty:
        WindDir = "SE"
elif 'NE' in forcastDirty:
        WindDir = "NE"
elif 'SW' in WindDirDirty:
        WindDir = "SW"
elif 'N' in WindDirDirty:
        WindDir = "N"
elif 'E' in WindDirDirty:
        WindDir = "E"
elif 'S' in WindDirDirty:
        WindDir = "S"
elif 'W' in WindDirDirty:
        WindDir = "W"
else:
        WindDir = "Error"
# Set current wind speed
WindSpdDirty = (curr_weaval[405:430]) #originally 410:430
WindSpd = re.sub("\D", "", WindSpdDirty)
#Set current precipitation possibility
precipDirty = (curr_weaval[255:275])
precip = re.sub("\D", "", precipDirty)
# DEF clock Updater
def clock():
    current = time.strftime("%-I %M %S").rjust(8," ")
    timeText.configure(text=current)
    root.after(1000, clock) # run every 1sec
#Set current Dew point
dewDirty = (curr_weaval[310:345]) #Pull section from current weather info
dewRaw = re.sub("\D", "", dewDirty) #Pull numbers from section
dewC = (dewRaw[0:2]) + "." + (dewRaw[3:5]) #Pull only 4 digits in form xx.xx. This is in celcius
dewC_S = float(dewC) #Convert string (dewC) to float data type 
dewF = (dewC_S * 1.8) + 32 #Convert C to F
dewF_S = str(dewF) #Convert F value to string
dew = (dewF_S[0:4]) #Finalize value by removing extra numbers from result
    
#Page 2 variables
debug_msg("Setting Page 2 Variables",1)
#Set general temp
       #Temp ranges
       #Less than 40 F Cold
       #41-60 F Cool
       #61-70 F Warm
       #71+ F Hot
temp_int = int(temp)
if temp_int <= 40:
     shortTemp = "COLD"
elif temp_int < 40 >= 60:
     shortTemp = "COOL"
elif temp_int < 60 >= 70:
     shortTemp = "WARM"
elif temp_int > 71:
     shortTemp = "HOT"
#Set rain possibility
      #Ranges
      # 0-40 Low
      #40.00001-60 Possible
      #60.00001-80 High
      #80+ Very Hih
precip_int = int(precip)
if precip_int <= 40:
       rainPoss = "LOW"
elif precip_int < 40 >= 60:
       rainPoss = "POSSIBLE"
elif precip_int < 60 >= 80:
       rainPoss = "HIGH"
elif precip_int < 80:
       rainPoss = "VERY HIGH"
#Determine wet/dry
if precip_int < 60:
       wetDry = "DRY"
elif precip_int > 60:
       wetDry = "POSSIBLY WET"

#Page 6 setup
debug_msg("Getting and Setting Page 6 Data and Variables",1)
Pg6_C1_Name = "DETROIT"
Pg6_C1_State = "MI"
Pg6_C1_Zip = 48127

n = NOAA()
res = n.get_forecasts(Pg6_C1_Zip, 'US')
for Pg6_C1 in res:
    Pg6_C1_curr_weaval = str(Pg6_C1) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg6_C1_forcastDirty = (Pg6_C1_curr_weaval[450:560]) #Originally 450:535
Pg6_C1_shortForcast = shortFDetermine(Pg6_C1_forcastDirty)
#Set current temp
Pg6_C1_tempDirty = (Pg6_C1_curr_weaval[140:150])
Pg6_C1_temp = re.sub("\D", "", Pg6_C1_tempDirty)

Pg6_C2_Name = "CAVE CITY"
Pg6_C2_State = "KY"
Pg6_C2_Zip = 42127

n = NOAA()
res = n.get_forecasts(Pg6_C2_Zip, 'US')
for Pg6_C2 in res:
    Pg6_C2_curr_weaval = str(Pg6_C2) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg6_C2_forcastDirty = (Pg6_C2_curr_weaval[450:560]) #Originally 450:535
Pg6_C2_shortForcast = shortFDetermine(Pg6_C2_forcastDirty)
#Set current temp
Pg6_C2_tempDirty = (Pg6_C2_curr_weaval[140:150])
Pg6_C2_temp = re.sub("\D", "", Pg6_C2_tempDirty)

Pg6_C3_Name = "N.Y. CITY"
Pg6_C3_State = "NY"
Pg6_C3_Zip = 10001

n = NOAA()
res = n.get_forecasts(Pg6_C3_Zip, 'US')
for Pg6_C3 in res:
    Pg6_C3_curr_weaval = str(Pg6_C3) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg6_C3_forcastDirty = (Pg6_C3_curr_weaval[450:560]) #Originally 450:535
Pg6_C3_shortForcast = shortFDetermine(Pg6_C3_forcastDirty)
#Set current temp
Pg6_C3_tempDirty = (Pg6_C3_curr_weaval[140:150])
Pg6_C3_temp = re.sub("\D", "", Pg6_C3_tempDirty)

Pg6_C4_Name = "SEATTLE"
Pg6_C4_State = "WA"
Pg6_C4_Zip = 98039

n = NOAA()
res = n.get_forecasts(Pg6_C4_Zip, 'US')
for Pg6_C4 in res:
    Pg6_C4_curr_weaval = str(Pg6_C4) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg6_C4_forcastDirty = (Pg6_C4_curr_weaval[450:560]) #Originally 450:535
Pg6_C4_shortForcast = shortFDetermine(Pg6_C4_forcastDirty)
#Set current temp
Pg6_C4_tempDirty = (Pg6_C4_curr_weaval[140:150])
Pg6_C4_temp = re.sub("\D", "", Pg6_C4_tempDirty)

Pg6_C5_Name = "CHICAGO"
Pg6_C5_State = "IL"
Pg6_C5_Zip = 60007

n = NOAA()
res = n.get_forecasts(Pg6_C5_Zip, 'US')
for Pg6_C5 in res:
    Pg6_C5_curr_weaval = str(Pg6_C5) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg6_C5_forcastDirty = (Pg6_C5_curr_weaval[450:560]) #Originally 450:535
Pg6_C5_shortForcast = shortFDetermine(Pg6_C5_forcastDirty)
#Set current temp
Pg6_C5_tempDirty = (Pg6_C5_curr_weaval[140:150])
Pg6_C5_temp = re.sub("\D", "", Pg6_C5_tempDirty)

Pg6_C6_Name = "MARIETTA"
Pg6_C6_State = "OH"
Pg6_C6_Zip = 47750

n = NOAA()
res = n.get_forecasts(Pg6_C6_Zip, 'US')
for Pg6_C6 in res:
    Pg6_C6_curr_weaval = str(Pg6_C6) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg6_C6_forcastDirty = (Pg6_C6_curr_weaval[450:560]) #Originally 450:535
Pg6_C6_shortForcast = shortFDetermine(Pg6_C6_forcastDirty)
#Set current temp
Pg6_C6_tempDirty = (Pg6_C6_curr_weaval[140:150])
Pg6_C6_temp = re.sub("\D", "", Pg6_C6_tempDirty)

Pg6_C7_Name = "TOLEDO"
Pg6_C7_State = "OH"
Pg6_C7_Zip = 43537

n = NOAA()
res = n.get_forecasts(Pg6_C7_Zip, 'US')
for Pg6_C7 in res:
    Pg6_C7_curr_weaval = str(Pg6_C7) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg6_C7_forcastDirty = (Pg6_C7_curr_weaval[450:560]) #Originally 450:535
Pg6_C7_shortForcast = shortFDetermine(Pg6_C7_forcastDirty)
#Set current temp
Pg6_C7_tempDirty = (Pg6_C7_curr_weaval[140:150])
Pg6_C7_temp = re.sub("\D", "", Pg6_C7_tempDirty)
# DEF main weather pages

#Page 7 setup
debug_msg("Getting and Setting Page 7 Data and Variables",1)
Pg7_C1_Name = "AUSTIN"
Pg7_C1_State = "TX"
Pg7_C1_Zip = 77301

n = NOAA()
res = n.get_forecasts(Pg7_C1_Zip, 'US')
for Pg7_C1 in res:
    Pg7_C1_curr_weaval = str(Pg7_C1) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg7_C1_forcastDirty = (Pg7_C1_curr_weaval[450:560]) #Originally 450:535
Pg7_C1_shortForcast = shortFDetermine(Pg7_C1_forcastDirty)
#Set current temp
Pg7_C1_tempDirty = (Pg7_C1_curr_weaval[140:150])
Pg7_C1_temp = re.sub("\D", "", Pg7_C1_tempDirty)

Pg7_C2_Name = "COLUMBUS"
Pg7_C2_State = "OH"
Pg7_C2_Zip = 43004

n = NOAA()
res = n.get_forecasts(Pg7_C2_Zip, 'US')
for Pg7_C2 in res:
    Pg7_C2_curr_weaval = str(Pg7_C2) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg7_C2_forcastDirty = (Pg7_C2_curr_weaval[450:560]) #Originally 450:535
Pg7_C2_shortForcast = shortFDetermine(Pg7_C2_forcastDirty)
#Set current temp
Pg7_C2_tempDirty = (Pg7_C2_curr_weaval[140:150])
Pg7_C2_temp = re.sub("\D", "", Pg7_C2_tempDirty)

Pg7_C3_Name = "MONT..ERY"
Pg7_C3_State = "AL"
Pg7_C3_Zip = 36043

n = NOAA()
res = n.get_forecasts(Pg7_C3_Zip, 'US')
for Pg7_C3 in res:
    Pg7_C3_curr_weaval = str(Pg7_C3) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg7_C3_forcastDirty = (Pg7_C3_curr_weaval[450:560]) #Originally 450:535
Pg7_C3_shortForcast = shortFDetermine(Pg7_C3_forcastDirty)
#Set current temp
Pg7_C3_tempDirty = (Pg7_C3_curr_weaval[140:150])
Pg7_C3_temp = re.sub("\D", "", Pg7_C3_tempDirty)

Pg7_C4_Name = "RALEIGH"
Pg7_C4_State = "NC"
Pg7_C4_Zip = 27513

n = NOAA()
res = n.get_forecasts(Pg7_C4_Zip, 'US')
for Pg7_C4 in res:
    Pg7_C4_curr_weaval = str(Pg7_C4) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg7_C4_forcastDirty = (Pg7_C4_curr_weaval[450:560]) #Originally 450:535
Pg7_C4_shortForcast = shortFDetermine(Pg7_C4_forcastDirty)
#Set current temp
Pg7_C4_tempDirty = (Pg7_C4_curr_weaval[140:150])
Pg7_C4_temp = re.sub("\D", "", Pg7_C4_tempDirty)

Pg7_C5_Name = "SACR..NTO"
Pg7_C5_State = "CA"
Pg7_C5_Zip = 95758

n = NOAA()
res = n.get_forecasts(Pg7_C5_Zip, 'US')
for Pg7_C5 in res:
    Pg7_C5_curr_weaval = str(Pg7_C5) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg7_C5_forcastDirty = (Pg7_C5_curr_weaval[450:560]) #Originally 450:535
Pg7_C5_shortForcast = shortFDetermine(Pg7_C5_forcastDirty)
#Set current temp
Pg7_C5_tempDirty = (Pg7_C5_curr_weaval[140:150])
Pg7_C5_temp = re.sub("\D", "", Pg7_C5_tempDirty)

Pg7_C6_Name = "TAL..SSEE"
Pg7_C6_State = "FL"
Pg7_C6_Zip = 32301

n = NOAA()
res = n.get_forecasts(Pg7_C6_Zip, 'US')
for Pg7_C6 in res:
    Pg7_C6_curr_weaval = str(Pg7_C6) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg7_C6_forcastDirty = (Pg7_C6_curr_weaval[450:560]) #Originally 450:535
Pg7_C6_shortForcast = shortFDetermine(Pg7_C6_forcastDirty)
#Set current temp
Pg7_C6_tempDirty = (Pg7_C6_curr_weaval[140:150])
Pg7_C6_temp = re.sub("\D", "", Pg7_C6_tempDirty)

Pg7_C7_Name = "WASHI. D.C."
Pg7_C7_State = " "
Pg7_C7_Zip = 20500

n = NOAA()
res = n.get_forecasts(Pg7_C7_Zip, 'US')
for Pg7_C7 in res:
    Pg7_C7_curr_weaval = str(Pg7_C7) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg7_C7_forcastDirty = (Pg7_C7_curr_weaval[450:560]) #Originally 450:535
Pg7_C7_shortForcast = shortFDetermine(Pg7_C7_forcastDirty)
#Set current temp
Pg7_C7_tempDirty = (Pg7_C7_curr_weaval[140:150])
Pg7_C7_temp = re.sub("\D", "", Pg7_C7_tempDirty)

#Page 8 setup
debug_msg("Getting and Setting Page 8 Data and Variables",1)
Pg8_C1_Name = "KILL D H"
Pg8_C1_State = "NC"
Pg8_C1_Zip = 27948

n = NOAA()
res = n.get_forecasts(Pg8_C1_Zip, 'US')
for Pg8_C1 in res:
    Pg8_C1_curr_weaval = str(Pg8_C1) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg8_C1_forcastDirty = (Pg8_C1_curr_weaval[450:560]) #Originally 450:535
Pg8_C1_shortForcast = shortFDetermine(Pg8_C1_forcastDirty)
#Set current temp
Pg8_C1_tempDirty = (Pg8_C1_curr_weaval[140:150])
Pg8_C1_temp = re.sub("\D", "", Pg8_C1_tempDirty)

Pg8_C2_Name = "HONOLULU"
Pg8_C2_State = "HI"
Pg8_C2_Zip = 96795

n = NOAA()
res = n.get_forecasts(Pg8_C2_Zip, 'US')
for Pg8_C2 in res:
    Pg8_C2_curr_weaval = str(Pg8_C2) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg8_C2_forcastDirty = (Pg8_C2_curr_weaval[450:560]) #Originally 450:535
Pg8_C2_shortForcast = shortFDetermine(Pg8_C2_forcastDirty)
#Set current temp
Pg8_C2_tempDirty = (Pg8_C2_curr_weaval[140:150])
Pg8_C2_temp = re.sub("\D", "", Pg8_C2_tempDirty)

Pg8_C3_Name = "LA ANG.ES"
Pg8_C3_State = "CA"
Pg8_C3_Zip = 90001

n = NOAA()
res = n.get_forecasts(Pg8_C3_Zip, 'US')
for Pg8_C3 in res:
    Pg8_C3_curr_weaval = str(Pg8_C3) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg8_C3_forcastDirty = (Pg8_C3_curr_weaval[450:560]) #Originally 450:535
Pg8_C3_shortForcast = shortFDetermine(Pg8_C3_forcastDirty)
#Set current temp
Pg8_C3_tempDirty = (Pg8_C3_curr_weaval[140:150])
Pg8_C3_temp = re.sub("\D", "", Pg8_C3_tempDirty)

Pg8_C4_Name = "LAS VEGAS"
Pg8_C4_State = "NV"
Pg8_C4_Zip = 89166

n = NOAA()
res = n.get_forecasts(Pg8_C4_Zip, 'US')
for Pg8_C4 in res:
    Pg8_C4_curr_weaval = str(Pg8_C4) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg8_C4_forcastDirty = (Pg8_C4_curr_weaval[450:560]) #Originally 450:535
Pg8_C4_shortForcast = shortFDetermine(Pg8_C4_forcastDirty)
#Set current temp
Pg8_C4_tempDirty = (Pg8_C4_curr_weaval[140:150])
Pg8_C4_temp = re.sub("\D", "", Pg8_C4_tempDirty)

Pg8_C5_Name = "MYRTLE BE"
Pg8_C5_State = "SC"
Pg8_C5_Zip = 29572

n = NOAA()
res = n.get_forecasts(Pg8_C5_Zip, 'US')
for Pg8_C5 in res:
    Pg8_C5_curr_weaval = str(Pg8_C5) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg8_C5_forcastDirty = (Pg8_C5_curr_weaval[450:560]) #Originally 450:535
Pg8_C5_shortForcast = shortFDetermine(Pg8_C5_forcastDirty)
#Set current temp
Pg8_C5_tempDirty = (Pg8_C5_curr_weaval[140:150])
Pg8_C5_temp = re.sub("\D", "", Pg8_C5_tempDirty)

Pg8_C6_Name = "NAGS HEAD"
Pg8_C6_State = "NC"
Pg8_C6_Zip = 27959

n = NOAA()
res = n.get_forecasts(Pg8_C6_Zip, 'US')
for Pg8_C6 in res:
    Pg8_C6_curr_weaval = str(Pg8_C6) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg8_C6_forcastDirty = (Pg8_C6_curr_weaval[450:560]) #Originally 450:535
Pg8_C6_shortForcast = shortFDetermine(Pg8_C6_forcastDirty)
#Set current temp
Pg8_C6_tempDirty = (Pg8_C6_curr_weaval[140:150])
Pg8_C6_temp = re.sub("\D", "", Pg8_C6_tempDirty)

Pg8_C7_Name = "NIAGRA F"
Pg8_C7_State = "NY"
Pg8_C7_Zip = 14301

n = NOAA()
res = n.get_forecasts(Pg8_C7_Zip, 'US')
for Pg8_C7 in res:
    Pg8_C7_curr_weaval = str(Pg8_C7) #Convert i to string, stored as Current_WeatherValue (curr_weaval)
    break

#Set current short forcast
Pg8_C7_forcastDirty = (Pg8_C7_curr_weaval[450:560]) #Originally 450:535
Pg8_C7_shortForcast = shortFDetermine(Pg8_C7_forcastDirty)
#Set current temp
Pg8_C7_tempDirty = (Pg8_C7_curr_weaval[140:150])
Pg8_C7_temp = re.sub("\D", "", Pg8_C7_tempDirty)

#Set page 9 precipitation values (Based on data from pages 6-8)
Pg6_C1_precipDirty = (Pg6_C1_curr_weaval[255:275])
Pg6_C1_precip = re.sub("\D", "", Pg6_C1_precipDirty)

Pg6_C3_precipDirty = (Pg6_C3_curr_weaval[255:275])
Pg6_C3_precip = re.sub("\D", "", Pg6_C3_precipDirty)

Pg6_C6_precipDirty = (Pg6_C6_curr_weaval[255:275])
Pg6_C6_precip = re.sub("\D", "", Pg6_C6_precipDirty)

Pg7_C5_precipDirty = (Pg7_C5_curr_weaval[255:275])
Pg7_C5_precip = re.sub("\D", "", Pg7_C5_precipDirty)

Pg7_C7_precipDirty = (Pg7_C7_curr_weaval[255:275])
Pg7_C7_precip = re.sub("\D", "", Pg7_C7_precipDirty)

Pg8_C2_precipDirty = (Pg8_C2_curr_weaval[255:275])
Pg8_C2_precip = re.sub("\D", "", Pg8_C2_precipDirty)

Pg8_C7_precipDirty = (Pg8_C7_curr_weaval[255:275])
Pg8_C7_precip = re.sub("\D", "", Pg8_C7_precipDirty)

debug_msg("Launching Screen Routine",1)
def weather_page(PageColour, PageNum):
    # pull in current seconds and minutes -- to be used to cycle the middle section every 30sec
    
    time_sec = time.localtime().tm_sec
    time_min = time.localtime().tm_min
    
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    months = [" ", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]    
    linebreak = ['\n']

    PageTotal = 11

    if (PageNum == 1):
        
        # ===================== Screen 1 =====================
       # PageNum = PageNum + 4 #remove to bring back page 2
        # Today's day/date + specific weather conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)             
        
        # create 8 lines of text     
        s1 = (" WINNIPEG " + Hour_String + " " + AM_PM + " " + (TZ_String[9:12]) + "  " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2 = "TEMP  " + temp + " F                " #Fixed
        s2 = s2[0:24] + " HIGH " + "?" + " F" #Fix?
        s3 = shortForcast + "                         " #Fixed
        s3 = s3[0:24] + "  LOW " + "?" + " C" #Fix?
        s4 = "       CHANCE OF PRECIP. " + precip + " %" #Fixed
        #s5 = "HUMID  " + humidity.rjust(5," ") + " %         "
        s5 = "HUMID " + humid + " %" + "        WIND " + WindDir + " " + WindSpd + " MPH"
        s6 = "VISBY"
        #s6 = visibstr[0:18] + windchildex.rjust(17," ")
        s7 = "DEW   " + dew + " F         " 
        s7 = s7[0:18] + "UV INDEX " + "?" 
        s8 = "PRESSURE " + "?" + " KPA"

    elif (PageNum == 2):

        # ===================== Screen 2 =====================
        # text forecast for 5 days - page 1 of 3
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
        PageNum = PageNum +3 #Added by TS to skip forcast continued pages, comment out or remove this line to bring them back

        s1 = "WINNIPEG CITY FORECAST".center(35," ")
        s2 = ("TODAY'S WEATHER WILL BE " + shortForcast + ".")
        s3 = ("TODAY WILL BE  A " + shortTemp + " DAY." + temp + " F")
        s4 = ("THERE IS A " + rainPoss + " CHANCE OF RAIN. " + precip + " %")
        s5 = ("WIND SPEEDS ARE " + WindSpd + " MPH" + " BLOWING " + WindDir + ".")
        s6 = ("THE HUMIDITY LEVEL FOR TODAY IS " + humid + " %.")
        s7 = ("OUTDOOR ACTIVITIES SHOULD BE " + shortTemp + " AND ")
        s8 = (wetDry + ".")

    elif (PageNum == 3):
    
        # ===================== Screen 3 =====================
        # text forecast for 5 days - page 2 of 3
        # Screen 1 must run first as it sets up variables
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
#        PageNum = PageNum + 3 Added by TS, first/failed attempt to skip this page
        
        # create 8 lines of text
        s1 = "WINNIPEG CITY FORECAST CONT'D".center(35," ")
        s2 = " " #Lines removed by TechSavvvvy, this page has been skipped
        s3 = " "
        s4 = " "
        s5 = " "
        s6 = " "
        s7 = " "
        s8 = " " 

    elif (PageNum == 4):
 
        # ===================== Screen 4 =====================
        # text forecast for 5 days - page 3 of 3 -- optional
        
            # create 8 lines of text       
            s1 = "WINNIPEG CITY FORECAST CONT'D".center(35," ")
            s2 = " " #Lines removed by TechSavvvvy, this page has been skipped
            s3 = " "
            s4 = " "
            s5 = " "
            s6 = " "
            s7 = " "
            s8 = " "
    
    elif (PageNum == 5):
    
        # ===================== Screen 5 =====================
        # Weather States
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)            

        # create 8 lines of text   
        s1 = ("TEMPERATURE STATISTICS FOR WINNIPEG").center(35," ")
        s2 = ("       CURRENT " + " C  ")
        s3 = " "
        s4 = "                 LOW    HIGH"
        s5 = ("        TODAY   " + " C  " + " C")
        s6 = ("    YESTERDAY   " + " C  " + temp_yest_high.rjust(3," ") + " C")
        s7 = ("       NORMAL   " + " C  "  + " C")
        s8 = " "
    
    elif (PageNum == 6):    
    
        # ===================== Screen 6 =====================
        # Manitoba and Regional Temperatures & Conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
        
        # create 8 lines of text   
        s1=("          " + Day + " " + Month + " " + Date_String + "/" + Year_String)
        s2=(Pg6_C1_Name + "," + Pg6_C1_State + "   " + Pg6_C1_temp + " F" + " " + Pg6_C1_shortForcast)
        s3=(Pg6_C2_Name + "," + Pg6_C2_State + " " + Pg6_C2_temp + " F" + " " + Pg6_C2_shortForcast)
        s4=(Pg6_C3_Name + "," + Pg6_C3_State + " " + Pg6_C3_temp + " F" + " " + Pg6_C3_shortForcast)
        s5=(Pg6_C4_Name + "," + Pg6_C4_State + "   " + Pg6_C4_temp + " F" + " " + Pg6_C4_shortForcast)
        s6=(Pg6_C5_Name + "," + Pg6_C5_State + "   " + Pg6_C5_temp + " F" + " " + Pg6_C5_shortForcast)
        s7=(Pg6_C6_Name + "," + Pg6_C6_State + "  " + Pg6_C6_temp + " F" + " " + Pg6_C6_shortForcast)
        s8=(Pg6_C7_Name + "," + Pg6_C7_State + "    " + Pg6_C7_temp + " F" + " " + Pg6_C7_shortForcast)

    elif (PageNum == 7):
    
        # ===================== Screen 7 =====================
        # Western Canada Temperatures & Conditions       
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
        
        # create 8 lines of text     
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg7_C1_Name + "," + Pg7_C1_State + "    " + Pg7_C1_temp + " F" + " " + Pg7_C1_shortForcast)
        s3=(Pg7_C2_Name + "," + Pg7_C2_State + "  " + Pg7_C2_temp + " F" + " " + Pg7_C2_shortForcast)
        s4=(Pg7_C3_Name + "," + Pg7_C3_State + " " + Pg7_C3_temp + " F" + " " + Pg7_C3_shortForcast)
        s5=(Pg7_C4_Name + "," + Pg7_C4_State + "   " + Pg7_C4_temp + " F" + " " + Pg7_C4_shortForcast)
        s6=(Pg7_C5_Name + "," + Pg7_C5_State + " " + Pg7_C5_temp + " F" + " " + Pg7_C5_shortForcast)
        s7=(Pg7_C6_Name + "," + Pg7_C6_State + " " + Pg7_C6_temp + " F" + " " + Pg7_C6_shortForcast)
        s8=(Pg7_C7_Name + "  " + Pg7_C7_temp + " F" + " " + Pg7_C7_shortForcast)
             
    elif (PageNum == 8):   
    
        # ===================== Screen 8 =====================
        # Eastern Canada Temperatures & Conditions       
        PageNum = PageNum + 1
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
        
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg8_C1_Name + "," + Pg8_C1_State + "  " + Pg8_C1_temp + " F" + " " + Pg8_C1_shortForcast)
        s3=(Pg8_C2_Name + "," + Pg8_C2_State + "  " + Pg8_C2_temp + " F" + " " + Pg8_C2_shortForcast)
        s4=(Pg8_C3_Name + "," + Pg8_C3_State + " " + Pg8_C3_temp + " F" + " " + Pg8_C3_shortForcast)
        s5=(Pg8_C4_Name + "," + Pg8_C4_State + " " + Pg8_C4_temp + " F" + " " + Pg8_C4_shortForcast)
        s6=(Pg8_C5_Name + "," + Pg8_C5_State + " " + Pg8_C5_temp + " F" + " " + Pg8_C5_shortForcast)
        s7=(Pg8_C6_Name + "," + Pg8_C6_State + " " + Pg8_C6_temp + " F" + " " + Pg8_C6_shortForcast)
        s8=(Pg8_C7_Name + "," + Pg8_C7_State + "  " + Pg8_C7_temp + " F" + " " + Pg8_C7_shortForcast)
    
    elif (PageNum == 9):
        
        # ===================== Screen 9 =====================
        # hourly forecast
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
 
        # get local timezone to show on screen
        local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        hrly_period_local = list(map(lambda x: x.astimezone(), hrly_period))

        # create 8 lines of text           
        s1 = ("WINNIPEG HOURLY FORECAST").center(35," ")
        s2 = " "
        s3 = " " 
        s4 = " "
        s5 = " "
        s6 = " "
        s7 = " " 
        s8 = " "
    
    elif (PageNum == 10):

        # ===================== Screen 10 =====================
        # preciptation page
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)        
    
        # create 8 lines of text   
        s1 = ("MANITOBA PRECIPITATION FORECAST").center(35," ")
        s2 =("          " + Pg6_C1_Name + "," + Pg6_C1_State + "       " + Pg6_C1_precip + " %")
        s3 =("          " + Pg6_C3_Name + "," + Pg6_C3_State + "     " + Pg6_C3_precip + " %")
        s4 =("          " + Pg6_C6_Name + "," + Pg6_C6_State + "      " + Pg6_C6_precip + " %")
        s5 =("          " + Pg7_C5_Name + "," + Pg7_C5_State + "     " + Pg7_C5_precip + " %")
        s6 =("          " + Pg7_C7_Name + "      " + Pg7_C7_precip + " %")
        s7 =("          " + Pg8_C2_Name + "," + Pg8_C2_State + "      " + Pg8_C2_precip + " %")
        s8 =("          " + Pg8_C7_Name + "," + Pg8_C7_State + "      " + Pg8_C7_precip + " %")

    elif (PageNum == 11):    
        
        # ===================== Screen 11 =====================
        # custom/extra page - currently used for my channel listing
        # to disable this page, set PageTotal to 10
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)         
      
        # create 8 lines of text

        s1 = "==========CHANNEL LISTING=========="
        s2 = "  2 SIMPSNS  13.1 CITY    50 SECUR"    
        s3 = "3.1 CBC FR.    14 90sTV   54 COMEDY" 
        s4 = "  6 60s/70s    16 TOONS   61 MUSIC"         
        s5 = "6.1 CBC        22 GLOBAL  64 WEATHR"
        s6 = "7.1 CTV        24 80sTV"
        s7 = "9.1 GLOBAL   35.1 FAITH"
        s8 = " 10 CBC        45 CHROMECAST" 

    # create the canvas for middle page text

    weather = Canvas(root, height=310, width=720, bg=PageColour)
    weather.place(x=0, y=85)
    weather.config(highlightbackground=PageColour)
    
    # place the 8 lines of text
    weather.create_text(80, 17, anchor='nw', text=s1, font=('VCR OSD Mono', 21, "bold"), fill="white")
    weather.create_text(80, 60, anchor='nw', text=s2, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 95, anchor='nw', text=s3, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 130, anchor='nw', text=s4, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 165, anchor='nw', text=s5, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 200, anchor='nw', text=s6, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 235, anchor='nw', text=s7, font=('VCR OSD Mono', 21,), fill="white") 
    weather.create_text(80, 270, anchor='nw', text=s8, font=('VCR OSD Mono', 21,), fill="white") 
    
    # Toggle Page Colour between Red & Blue
    if (PageColour == "blue"): # blue removed # from "#blue"
        PageColour = "#6D0000" # red
    else:
        PageColour = "blue" # blue removed #
        
    # Increment Page Number or Reset
    if (PageNum < PageTotal):
        PageNum = PageNum + 1
    elif (PageNum >= PageTotal):
        PageNum = 1
    
    root.after(20000, weather_page, PageColour, PageNum) # re-run every 20sec from program launch


# DEF bottom marquee scrolling text
def bottom_marquee(grouptotal):

    group = 1

    # scrolling text canvas
    marquee = Canvas(root, height=120, width=580, bg="green")
    marquee.config(highlightbackground="green")
    marquee.place(x=80, y=400)

    # read in RSS data and prepare it
    width = 35
    pad = ""
    for r in range(width): #create an empty string of 35 characters
        pad = pad + " " 

    url = "https://www.wkyc.com/feeds/syndication/rss/news/local"
    wpg = feedparser.parse(url)
    debug_msg("BOTTOM_MARQUEE-RSS feed refreshed",1)

    # Add first entry to string without padding
    wpg_desc = pad + wpg.entries[0]["description"]
    
    # Append all other RSS entry descriptions, with 35 character padding in between
    for n in range(len(wpg.entries)):
        if (n == 0) or ((len(wpg_desc + pad + wpg.entries[n]["description"]) * 24) >= 31000): # avoid duplicate first entry / check if string will be max pixels allowed
            n = n + 1
        else:
            wpg_desc = wpg_desc + pad + wpg.entries[n]["description"]
    
    # convert to upper case
    mrq_msg = wpg_desc.upper()

    # use the length of the news feeds to determine the total pixels in the scrolling section
    marquee_length = len(mrq_msg)
    pixels = marquee_length * 24 # roughly 24px per char

    # setup scrolling text
    text = marquee.create_text(1, 2, anchor='nw', text=pad + mrq_msg + pad, font=('VCR OSD Mono', 25,), fill="white")

    restart_marquee = True # 
    while restart_marquee:
        restart_marquee = False
        debug_msg("BOTTOM_MARQUEE-starting RSS display",1)
        for p in range(pixels+730):
            marquee.move(text, -1, 0) #shift the canvas to the left by 1 pixel
            marquee.update()
            time.sleep(0.002) # scroll every 2ms
            if (p == pixels+729): # once the canvas has finished scrolling
                restart_marquee = True
                marquee.move(text, pixels+729, 0) # reset the location
                if (group <= grouptotal):
                    debug_msg("BOTTOM_MARQUEE-launching weather update",1)
                    try:
                        weather_update(group) # update weather information between RSS scrolls
                        debug_msg("BOTTOM_MARQUEE-weather info refreshed",1)
                        group = group + 1
                    except:
                        debug_msg("BOTTOM_MARQUEE-ENV_CANADA_ERROR! weather info NOT refreshed",1)
                else:
                    debug_msg("BOTTOM_MARQUEE-launching weather update",1)
                    group = 1
                    try:
                        weather_update(group) # update weather information between RSS scrolls
                        debug_msg("BOTTOM_MARQUEE-weather info refreshed",1)
                        group = group + 1
                    except:
                        debug_msg("BOTTOM_MARQUEE-ENV_CANADA_ERROR! weather info NOT refreshed",1)
                    
                p = 0 # keep the for loop from ending
                wpg = feedparser.parse(url)
                debug_msg("BOTTOM_MARQUEE-RSS feed refreshed",1)

# DEF generate playlist from folder
def playlist_generator(musicpath):

    # this code from https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    # create a list of file and sub directories 
    # names in the given directory 

    debug_msg("PLAYLIST_GENERATOR-searching for music files...",1)
    filelist = os.listdir(musicpath)
    allFiles = list()
    # Iterate over all the entries    
    for entry in filelist:
        # Create full path
        fullPath = os.path.join(musicpath,entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + playlist_generator(fullPath)
        else:
            allFiles.append(fullPath)
    debug_msg(("PLAYLIST_GENERATOR-found " + str(len(allFiles))),1)
    return allFiles

# DEF play background music
def music_player(songNumber, playlist, musicpath):

    # make sure musicpath ONLY contains playable mp3 files. this does not check if files are valid and will crash if it tries to play something else

    if ((pygame.mixer.music.get_busy() == False) and (songNumber < len(playlist))):
        debug_msg(("MUSIC_PLAYER-playing song " + playlist[songNumber]),1)
        pygame.mixer.music.load(playlist[songNumber])
        pygame.mixer.music.play(loops = 0)
        songNumber = songNumber + 1
    elif ((pygame.mixer.music.get_busy() == False) and (songNumber >= len(playlist))):
        debug_msg("MUSIC_PLAYER-playlist complete,re-shuffling... ",1)
        songNumber = 0
        random.shuffle(playlist)   

    root.after(2000, music_player, songNumber, playlist, musicpath) # re-run every 2sec from program launch


# ROOT main stuff

# setup root
root = Tk()
root.attributes('-fullscreen',True)
root.geometry("720x480") # this must be 720x480 for a proper filled out screen on composite output. 640x480 will have black bar on RH side. use 720x576 for PAL.
root.config(cursor="none", bg="green")
root.wm_title("wpg-weatherchan")

# Clock - Top RIGHT
# this got complicated due to the new font (7-Segment Normal), which doesn't have proper colon(:) char, 
# so I've removed the colon from the time string and added them on top using VCR OSD Mono
debug_msg("ROOT-placing clock",1)
timeText = Label(root, text="", font=("7-Segment Normal", 22), fg="white", bg="green")
timeText.place(x=403, y=40)
timeColon1 = Label(root, text=":", font=("VCR OSD Mono", 32), fg="white", bg="green")
timeColon1.place(x=465, y=36)
timeColon2 = Label(root, text=":", font=("VCR OSD Mono", 32), fg="white", bg="green")
timeColon2.place(x=560, y=36)
debug_msg("ROOT-launching clock updater",1)
clock()

# Title - Top LEFT
debug_msg("ROOT-placing Title Text",1)
Title = Label(root, text="ENVIRONMENT USA", font=("VCR OSD Mono", 22, "bold"), fg="white", bg="green")
Title.place(x=0, y=40)

# total number of groups broken up to update sections of weather data, to keep update time short
grouptotal = 3 

# Middle Section (Cycling weather pages, every 30sec)
debug_msg("ROOT-launching weather_page",1)
PageColour = "blue" # blue
PageNum = 1
weather_page(PageColour, PageNum)

# Generate background music playlist
debug_msg("ROOT-launching playlist generator",1)
musicpath = "/home/techsavvvvy/Music" # must show full path
playlist = playlist_generator(musicpath) # generate playlist array
random.shuffle(playlist) # shuffle playlist

# Play background music on shuffle using pygame
debug_msg("ROOT-launching background music",1)
songNumber = 1
pygame.mixer.init()
music_player(songNumber, playlist, musicpath)

# Bottom Scrolling Text (City of Winnipeg RSS Feed)
debug_msg("ROOT-launching bottom_marquee",1)
bottom_marquee(grouptotal)

# loop program  
root.mainloop()

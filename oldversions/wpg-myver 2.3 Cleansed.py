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
import linecache

prog = "wpg-usa"
ver = "2.3"
Music = OFF #Ebables or disables music player, ON to turn it on, and anyhing else to disable it
#probnot's Retro Winnipeg Weather Channel USA version by TechSavvvvy
#Started on June 27, 2024, last updated July 14, 2024

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
# V 2.0
     #Added statements to shortFDetermine function
     #Added Music variable/switch, to turn music play on/off
     #Adjusted shortForcast range
     #Added sections to pull extra NOAA information
     #Brought back Pressure and Visiblity
     #Changed design of page one
     #Fixed an issue with the shortTemp if/elif statements, which if it wasn't HOT or COLD it would cause a crash on page one
     #Increased from 1048 to 1096 lines
# V 2.1
     #Fixed an issue where a humidity number using 3 digits with a decimal would be displayed as being over 100%. Ex instead of being 42.8%, it was 428%
     #Fixed an issue where no wind speed would show if there was no wind. This is correct, however, a 0 is more appropriate
     #Fixed an issue where the program wouldn't run at noon because of the way time determination was written. 
     #Changed "Slight Chance of Rain" to "Chance of Rain"
     #Fixed pages 6-8 to show full city names. The X value for text can now be changed on a per page basis
     #Added Page 3 Weekly Forecast
     #Increased from 1096 to 1212 lines
#V2.2
    #Moved all variables to beginning of code
    #Replaced individual sections pulling weather data for each city with one function
    #Replaced individual lines determining temp with one function
    #Added line to shortFDetermine to automatically create dirty forecast line, instead of each section doing it individually
    #Added precipDetermine function
    #Replaced page 3 dedicated functions added in V2.1 with global functions listed above
    #Decreased from 1212 lines to 1085 lines
#V2.3
    #Reorganized code, moved all functions towards top
    #Moved screen code to if/elif statements running screens, as it was with probnot's version
    #Added several functions, basically anything that determines weather data is now a function
    #Decreased from 1085 to 1042 lines
#Fixes
     # Fix mispellings of Forecast (not forcast)
     # Make page 3 not rely on text file that needs to be manually generated
     #Fix issue showing 0 AM at midnight
ZIP = 97035 #Enter USA ZIP code here, added by -TS, TX-75007 Kill Devil Hills 27948

Pg6_C1_Name = "DETRIOT" #Set city name for the first city on page 6, used only for looks
Pg6_C1_State = "MI" #Set 2 digit state abbreviation for first city on page 6, also only used for looks
Pg6_C1_Zip = 48127 #Zip code for first city on page 6, used by NOAA to determine weather data

Pg6_C2_Name = "CAVE CITY" # From here on it repeats itself
Pg6_C2_State = "KY"
Pg6_C2_Zip = 42127

Pg6_C3_Name = "N.Y. CITY"
Pg6_C3_State = "NY"
Pg6_C3_Zip = 10001

Pg6_C4_Name = "SEATTLE"
Pg6_C4_State = "WA"
Pg6_C4_Zip = 98039

Pg6_C5_Name = "CHICAGO"
Pg6_C5_State = "IL"
Pg6_C5_Zip = 60007

Pg6_C6_Name = "MARIETTA"
Pg6_C6_State = "OH"
Pg6_C6_Zip = 47750

Pg6_C7_Name = "TOLEDO"
Pg6_C7_State = "OH"
Pg6_C7_Zip = 43537

Pg7_C1_Name = "AUSTIN"
Pg7_C1_State = "TX"
Pg7_C1_Zip = 77301

Pg7_C2_Name = "COLUMBUS"
Pg7_C2_State = "OH"
Pg7_C2_Zip = 43004

Pg7_C3_Name = "MONTGOMERY"
Pg7_C3_State = "AL"
Pg7_C3_Zip = 36043

Pg7_C4_Name = "RALEIGH"
Pg7_C4_State = "NC"
Pg7_C4_Zip = 27513

Pg7_C5_Name = "SACRAMENTO"
Pg7_C5_State = "CA"
Pg7_C5_Zip = 95758

Pg7_C6_Name = "TALLAHASSEE"
Pg7_C6_State = "FL"
Pg7_C6_Zip = 32301

Pg7_C7_Name = "WASHINGTON D.C."
Pg7_C7_State = " "
Pg7_C7_Zip = 20500

Pg8_C1_Name = "KILL DEVIL HILLS"
Pg8_C1_State = "NC"
Pg8_C1_Zip = 27948

Pg8_C2_Name = "HONOLULU"
Pg8_C2_State = "HI"
Pg8_C2_Zip = 96795

Pg8_C3_Name = "LA ANGELES"
Pg8_C3_State = "CA"
Pg8_C3_Zip = 90001

Pg8_C4_Name = "LAS VEGAS"
Pg8_C4_State = "NV"
Pg8_C4_Zip = 89166

Pg8_C5_Name = "MYRTLE BEACH"
Pg8_C5_State = "SC"
Pg8_C5_Zip = 29572

Pg8_C6_Name = "NAGS HEAD"
Pg8_C6_State = "NC"
Pg8_C6_Zip = 27959

Pg8_C7_Name = "NIAGRA FALLS"
Pg8_C7_State = "NY"
Pg8_C7_Zip = 14301

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

# DEF clock Updater Written by probnot
def clock():
    current = time.strftime("%-I %M %S").rjust(8," ")
    timeText.configure(text=current)
    root.after(1000, clock) # run every 1sec

def pullData(pullZip): #Use NOAA to retrive weather data
      n = NOAA()
      res = n.get_forecasts(pullZip, 'US')
      for i in res:
          Data = str(i) #Convert i to string, stored as Current_WeatherValue (curr_weaval). All data from NOAA is in one REALLY long string and must be broken down/extracted
          break
      return Data

def shortFDetermine(FDetIn): #Used to determine forcast, called by pages 1-3, 6-8 (4 and 5 are currently disabled)
     dirtyIn = FDetIn[450:580]
     if 'Mostly Clear' in dirtyIn: #dirtyIn will contain the forcast, and other garbage info, this is used to remove the garbage info
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
     elif 'Slight Chance Rain Showers' in dirtyIn:
        return "CHANCE OF RAIN"
     elif 'Chance Rain Showers' in dirtyIn:
        return "CHANCE OF RAIN"
     elif 'Rain Showers Likely' in dirtyIn:
        return "RAIN LIKELY"
     elif 'Rain' in dirtyIn:
        print("General Rain forcast used for" + dirtyIn)
        return "RAIN" #Used as general catch all for anything with rain
     elif 'Storm' in dirtyIn:
        print("General Storm forcast used for" + dirtyIn)
        return "STORM" #Used as general catch all for anything with rain
     elif 'Slight Chance Showers' in dirtyIn:
        return "POSSIBLE RAIN"
     elif 'Shower' in dirtyIn:
        print("General Shower forecast used for" + dirtyIn)
        return "RAIN"
     else:
        print("Unknown Forcast" + dirtyIn)
        return "ERROR"

def tempDetermine(dirty_TempIn):
        tempDirty = (dirty_TempIn[140:150]) #Isloates a section of the long string of data from NOAA, temp value will be surrounded by garbage data
        tempClean = re.sub("\D", "", tempDirty) #Pulls only numbers from data, so in theory only the temp value will be left
        return tempClean

def precipDetermine(dirty_precipIn): #Works similar to tempDetermine
        precipDirty = (dirty_precipIn[255:275])
        precipClean = re.sub("\D", "", precipDirty)
        return precipClean

#Set current humidity. Works similar to tempDetermine function.
def humidDetermine(humidIn):
    humidDirty = (humidIn[355:405])
    humidNums = re.sub("\D", "", humidDirty)
    humidOut = (humidNums[0:2])
    return humidOut

#Set current Wind Speed #Works similar to shortFDetermine function
def WinDirDetermine(windDirtyIn):
    WindDirDirty = (windDirtyIn[420:475])
    if 'SE' in WindDirDirty:
            return "SE"
    elif 'NE' in WindDirDirty:
            return "NE"
    elif 'SW' in WindDirDirty:
            return "SW"
    elif 'N' in WindDirDirty:
            return "N"
    elif 'E' in WindDirDirty:
            return "E"
    elif 'S' in WindDirDirty:
            return "S"
    elif 'W' in WindDirDirty:
            return "W"
    else:
            return "Error"

def WindSpdDetermine(WindSpdIn):
    WindSpdDirty = (WindSpdIn[405:430]) #originally 410:430 #Works similar to tempDetermine function
    WindStr = re.sub("\D", "", WindSpdDirty)
    Windint = WindStr
    if Windint.isdigit():
         return str(Windint)
    else:
        return str(0)

def dewDetermine(dewIn):
    dewDirty = (dewIn[310:345]) #Pull section from current weather info
    dewRaw = re.sub("\D", "", dewDirty) #Pull numbers from section
    dewC = (dewRaw[0:2]) + "." + (dewRaw[3:5]) #Pull only 4 digits in form xx.xx. This is in celcius
    dewC_S = float(dewC) #Convert string (dewC) to float data type 
    dewF = (dewC_S * 1.8) + 32 #Convert C to F
    dewF_S = str(dewF) #Convert F value to string
    dewOut = (dewF_S[0:4]) #Finalize value by removing extra numbers from result
    return dewOut

def pressureDetermine(pressureIn):
    pressureDirty = (pressureIn[950:1050]) #Works similar to setting current temp
    pressureNum = re.sub("\D", "", pressureDirty)
    PressureOut = (pressureNum[0:3] + "." + pressureNum[4:5]) #Puts pressure in xxx.x format
    return PressureOut

def visDetermine(visIn):
    visDirty = (visIn[1100:1200]) #Works similar to setting current temp
    visNum = re.sub("\D", "", visDirty)
    VisibilityOut = (visNum[0:2]) #Pulls only first 2 digits
    return VisibilityOut

#Set rain possibility
      #Ranges
      # 0-40 Low
      #40.00001-60 Possible
      #60.00001-80 High
      #80+ Very Hih
def rainPossDetermine(rainPossIn):
    precip_int = int(rainPossIn) #Set rain possibility page on precipitation percentage for page 2 forcast
    if precip_int <= 40: #Checks if temp is 40 F or below
           return "LOW" #If 40 or below, LOW possibility
    elif precip_int < 40 >= 60: #Checks if temp is 41-60 F
           return "POSSIBLE" #IF 41-60, POSSIBLE possibility
    elif precip_int < 60 >= 80: #61-80 F
           return "HIGH" #HIGH possibility
    elif precip_int < 80: #80 or above
           return "VERY HIGH" #VERY HIGH possibility

#Set general temp
       #Temp ranges
       #Less than 40 F Cold
       #41-60 F Cool
       #61-70 F Warm
       #71+ F Hot
def shortTempDetermine(tempIn):
    temp_int = int(tempIn) #Sets general/short temp for page two forcast using different ranges of temperature
    if temp_int <= 40:
         return "COLD"
    elif temp_int > 40 and temp_int <= 60:
         return "COOL"
    elif temp_int > 60 and temp_int <= 70:
         return "WARM"
    elif temp_int > 71:
         return "HOT"
    else:
         return "Error"

#Determine wet/dry, works similar to above
def wetDryDetermine(wetDryIn):
    wetDryInt = int(wetDryIn)
    if wetDryInt < 60:
           return "DRY"
    elif wetDryInt > 60:
           return "POSSIBLY WET"

#Obtaining weather data from NWS/NOAA
#Get page 1 and 2 weather data
debug_msg("Getting Page 1 and 2 Weather Data",1)
curr_weaval = pullData(ZIP)
#Set weather data for pages 6-8
debug_msg("Getting Page 6 data",1)
Pg6_C1_curr_weaval = pullData(Pg6_C1_Zip) #Uses pullData function to pull weather data from NOAA
Pg6_C2_curr_weaval = pullData(Pg6_C2_Zip)
Pg6_C3_curr_weaval = pullData(Pg6_C3_Zip)
Pg6_C4_curr_weaval = pullData(Pg6_C4_Zip)
Pg6_C5_curr_weaval = pullData(Pg6_C5_Zip)
Pg6_C6_curr_weaval = pullData(Pg6_C6_Zip)
Pg6_C7_curr_weaval = pullData(Pg6_C7_Zip)
debug_msg("Getting Page 7 data",1)
Pg7_C1_curr_weaval = pullData(Pg7_C1_Zip)
Pg7_C2_curr_weaval = pullData(Pg7_C2_Zip)
Pg7_C3_curr_weaval = pullData(Pg7_C3_Zip)
Pg7_C4_curr_weaval = pullData(Pg7_C4_Zip)
Pg7_C5_curr_weaval = pullData(Pg7_C5_Zip)
Pg7_C6_curr_weaval = pullData(Pg7_C6_Zip)
Pg7_C7_curr_weaval = pullData(Pg7_C7_Zip)
debug_msg("Getting Page 8 data",1)
Pg8_C1_curr_weaval = pullData(Pg8_C1_Zip)
Pg8_C2_curr_weaval = pullData(Pg8_C2_Zip)
Pg8_C3_curr_weaval = pullData(Pg8_C3_Zip)
Pg8_C4_curr_weaval = pullData(Pg8_C4_Zip)
Pg8_C5_curr_weaval = pullData(Pg8_C5_Zip)
Pg8_C6_curr_weaval = pullData(Pg8_C6_Zip)
Pg8_C7_curr_weaval = pullData(Pg8_C7_Zip)

#Set current date/time
current_time = datetime.datetime.now() #This outputs the month as a number, 1 being January and 12 being December, the if/elif is used to translate the number to a shortened verison of the name
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
if current_time.hour > 12: #current_time.hour is in 24 hour/military time, this line detects if it's past 12:00 PM (not AM)
     Hour = current_time.hour - 12 #Subtracts 12 from hour if it's after 12, converting from military time to AM/PM time
     AM_PM = "PM" #Tells program to show PM on page 1
elif current_time.hour < 12: # Detects if time is befrom 12:00 pm
     Hour = current_time.hour #Sets Hour variable to current hour, no math is needed
     AM_PM = "AM" #Tells program to show PM on page 1
elif current_time.hour == 12: # Detects if time is 12:00 pm
     Hour = current_time.hour #Sets Hour variable to current hour, no math is needed
     AM_PM = "PM" #Tells program to show PM on page 1
else:
     Hour = "ER" #Failure message in case something goes wrong, this should never happen
Hour_String = str(Hour)

#Determine Weekday
if current_time.weekday() == 0: #Determines day of week, this is similar to the way month is determined, 0 is Monday and 6 is Sunday
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
Date_String = str(current_time.day) #Find currrent date, just the date itself. In other words, it's not determining "07-20-2024", it would determine that it's the 20th
if current_time.day < 10: #Detects if it's before the 10th
    Date = ("0" + Date_String) #If it's before the 10th, a "0" will be added in front of it, ex. changing 8 to 08. Used for NOAA and looks. 
else:
    Date = Date_String

#Set current year
Year_String = str(current_time.year)

#Build current date in YYYY-MM-DD form to obtain more data from NOOAA
Month_Str = str(current_time.month) #Month value needs to be in string form for this to work
if current_time.month < 10: #Determines if month is a 1 digit value
    Month_Num = ("0" + Month_Str) #Adds 0 in front of month value, ex. instead of January being 1, it would be 01. Needed for NOAA
else:
    Month_Num = Month_Str #ignores above for months with 2 digit value
T_Date = (Year_String + "-" + Month_Num + "-" + Date) #Builds data value in YYYY-MM-DD form

#Get extra forcast data 
n = NOAA()
observations = n.get_observations(ZIP,'US',start=T_Date,end=T_Date)
for Today_Data in observations:
    Today_Data_Dirty = str(Today_Data)
    break

#Shared data
temp = tempDetermine(curr_weaval)
WindDir = WinDirDetermine(curr_weaval)
WindSpd = WindSpdDetermine(curr_weaval)
humid = humidDetermine(curr_weaval)
precip = precipDetermine(curr_weaval)
shortForcast = shortFDetermine(curr_weaval)

debug_msg("Launching Screen Routine",1) #Used to send message to CLI that the screen routine will begin, also let's you know all weather data has been successfully obtained
def weather_page(PageColour, PageNum): #Written by probnot
    # pull in current seconds and minutes -- to be used to cycle the middle section every 30sec
    
    time_sec = time.localtime().tm_sec
    time_min = time.localtime().tm_min
    
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    months = [" ", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]    
    linebreak = ['\n']

    PageTotal = 11
    if (PageNum == 1):
        # ===================== Screen 1 =====================
        #  PageNum = PageNum + 1 #remove to bring back page 2
        dew = dewDetermine(curr_weaval)
        Pressure = pressureDetermine(Today_Data_Dirty)
        Visibility = visDetermine(Today_Data_Dirty)
        # Today's day/date + specific weather conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)             
        X_VAL = 80
        # create 8 lines of text     
        s1 = (" WINNIPEG " + Hour_String + " " + AM_PM + " " + (TZ_String[9:12]) + "  " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2 = ("TEMP  " + temp + " F" + "            WIND " + WindDir + " " + WindSpd + " MPH") #Fixed
        # s2 = s2[0:24] + " HIGH " + "?" + " F" Removed due to NOAA not showing High temp
        s3 = shortForcast + "                         " #Fixed
        # s3 = s3[0:24] + "  LOW " + "?" + " C" #Fix? Removed due to NOAA not showing Low temp
        s4 = "       CHANCE OF PRECIP. " + precip + " %" 
        #s5 = "HUMID  " + humidity.rjust(5," ") + " %         "
        s5 = "HUMID " + humid + " %" 
        s6 = ("VISBY " + Visibility + " MI")
        #s6 = visibstr[0:18] + windchildex.rjust(17," ")
        s7 = "DEW   " + dew + " F         " 
        # s7 = s7[0:18] + "UV INDEX " + "?" Removed due to NOAA not UV Index 
        s8 = "PRESSURE " + Pressure + " KPA"

    elif (PageNum == 2):

        # ===================== Screen 2 =====================
        shortTemp = shortTempDetermine(temp)
        rainPoss = rainPossDetermine(precip)
        wetDry = wetDryDetermine(precip)
        # text forecast for 5 days - page 1 of 3
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
       # PageNum = PageNum +3 #Added by TS to skip forcast continued pages, comment out or remove this line to bring them back
        X_VAL = 80
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
        PageNum = PageNum + 2
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
        def Weekday (dayNum): #Used to determine day of the week
           if dayNum >= 7: #Checks if value is 7 or more. Read 2 comments down to understand this. This is here because for example, a value of 5 is Saturday, 3 days away is Tuesday. 5+3 = 8. 8 is not a valid response in this case. However, 8-7 = 1, and 1 is Tuesday. Therefore this is used for when the current day is later in the week
               dayNum = dayNum - 7 #Subtracts 7 if necessary
               if dayNum == 0: #Determines day of week, this is similar to the way month is determined, 0 is Monday and 6 is Sunday
                  return "MONDAY     "
               elif dayNum == 1:
                  return "TUESDAY    "
               elif dayNum == 2:
                  return "WEDNESDAY  "
               elif dayNum == 3:
                  return "THURSDAY   "
               elif dayNum == 4:
                  return "FRIDAY     "
               elif dayNum == 5:
                  return "SATURDAY   "
               elif dayNum == 6:
                  return "SUNDAY     "
           else:
               dayNum = dayNum
               if dayNum == 0: #Determines day of week, this is similar to the way month is determined, 0 is Monday and 6 is Sunday
                  return "MONDAY     "
               elif dayNum == 1:
                  return "TUESDAY    "
               elif dayNum == 2:
                  return "WEDNESDAY  "
               elif dayNum == 3:
                  return "THURSDAY   "
               elif dayNum == 4:
                  return "FRIDAY     "
               elif dayNum == 5:
                  return "SATURDAY   "
               elif dayNum == 6:
                  return "SUNDAY     "
        DayNum = current_time.weekday() # Get current weekday value from system
        day_1_dayNum = DayNum + 1 # These lines determine the next days of the week. It takes the current day value (0-6) and adds a number accordingly
        day_2_dayNum = DayNum + 2
        day_3_dayNum = DayNum + 3
        day_4_dayNum = DayNum + 4
        day_5_dayNum = DayNum + 5
        day_6_dayNum = DayNum + 6
        day_7_dayNum = DayNum + 7

        day_1 = Weekday(day_1_dayNum) #Calls Weekday function to determine day of the week
        day_2 = Weekday(day_2_dayNum)
        day_3 = Weekday(day_3_dayNum)
        day_4 = Weekday(day_4_dayNum)
        day_5 = Weekday(day_5_dayNum)
        day_6 = Weekday(day_6_dayNum)
        day_7 = Weekday(day_7_dayNum)

        filename = '/tmp/future.txt'
        Pg3_day_1_Weaval = linecache.getline(filename, 25) #Pulls lines from text file for weather data during the week
        Pg3_day_2_Weaval = linecache.getline(filename, 49)
        Pg3_day_3_Weaval = linecache.getline(filename, 73)
        Pg3_day_4_Weaval = linecache.getline(filename, 97)
        Pg3_day_5_Weaval = linecache.getline(filename, 121)
        Pg3_day_6_Weaval = linecache.getline(filename, 145)

        Pg3_day_1_Forecast = shortFDetermine(Pg3_day_1_Weaval) #Calls forecast function to determine forecast for each day
        Pg3_day_2_Forecast = shortFDetermine(Pg3_day_2_Weaval)
        Pg3_day_3_Forecast = shortFDetermine(Pg3_day_3_Weaval)
        Pg3_day_4_Forecast = shortFDetermine(Pg3_day_4_Weaval)
        Pg3_day_5_Forecast = shortFDetermine(Pg3_day_5_Weaval)
        Pg3_day_6_Forecast = shortFDetermine(Pg3_day_6_Weaval)

        Pg3_day_1_temp = tempDetermine(Pg3_day_1_Weaval) #Calls temperature function to determine temperature for each day
        Pg3_day_2_temp = tempDetermine(Pg3_day_2_Weaval)
        Pg3_day_3_temp = tempDetermine(Pg3_day_3_Weaval)
        Pg3_day_4_temp = tempDetermine(Pg3_day_4_Weaval)
        Pg3_day_5_temp = tempDetermine(Pg3_day_5_Weaval)
        Pg3_day_6_temp = tempDetermine(Pg3_day_6_Weaval)

        Pg3_day_1_Precip = precipDetermine(Pg3_day_1_Weaval) #Calls precipitation function to determine precipitation for each day
        Pg3_day_2_Precip = precipDetermine(Pg3_day_2_Weaval)
        Pg3_day_3_Precip = precipDetermine(Pg3_day_3_Weaval)
        Pg3_day_4_Precip = precipDetermine(Pg3_day_4_Weaval)
        Pg3_day_5_Precip = precipDetermine(Pg3_day_5_Weaval)
        Pg3_day_6_Precip = precipDetermine(Pg3_day_6_Weaval)
#        PageNum = PageNum + 3 Added by TS, first/failed attempt to skip this page
        X_VAL = 0
        # create 8 lines of text
        s1 = "WEEK FORECAST".center(35," ")
        s2 = ("TODAY      " + temp + " F " + "Rain: " + precip + "% " + shortForcast)
        s3 = (day_1 + Pg3_day_1_temp + " F " + "Rain: " + Pg3_day_1_Precip + "% " + Pg3_day_1_Forecast)
        s4 = (day_2  + Pg3_day_2_temp + " F " + "Rain: " + Pg3_day_2_Precip + "% " + Pg3_day_2_Forecast)
        s5 = (day_3 + Pg3_day_3_temp + " F " + "Rain: " + Pg3_day_3_Precip + "% " + Pg3_day_3_Forecast)
        s6 = (day_4 + Pg3_day_4_temp + " F " + "Rain: " + Pg3_day_4_Precip + "% " + Pg3_day_4_Forecast)
        s7 = (day_5 + Pg3_day_5_temp + " F " + "Rain: " + Pg3_day_5_Precip + "% " + Pg3_day_5_Forecast)
        s8 = (day_6 + Pg3_day_6_temp + " F " + "Rain: " + Pg3_day_6_Precip + "% " + Pg3_day_6_Forecast)

    elif (PageNum == 4):
 
        # ===================== Screen 4 =====================
        # text forecast for 5 days - page 3 of 3 -- optional
            X_VAL = 80
            # create 8 lines of text       
            s1 = "WEEK FORECAST".center(35," ")
            s2 = " " 
            s3 = " '"
            s4 = " "
            s5 = " "
            s6 = " "
            s7 = " "
            s8 = " "
    
    elif (PageNum == 5):
    
        # ===================== Screen 5 =====================
        # Weather States
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)            
        X_VAL = 80
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
        
        #Set current short forcast
        Pg6_C1_shortForcast = shortFDetermine(Pg6_C1_curr_weaval)
        Pg6_C2_shortForcast = shortFDetermine(Pg6_C2_curr_weaval)
        Pg6_C3_shortForcast = shortFDetermine(Pg6_C3_curr_weaval)
        Pg6_C4_shortForcast = shortFDetermine(Pg6_C4_curr_weaval)
        Pg6_C5_shortForcast = shortFDetermine(Pg6_C5_curr_weaval)
        Pg6_C6_shortForcast = shortFDetermine(Pg6_C6_curr_weaval)
        Pg6_C7_shortForcast = shortFDetermine(Pg6_C7_curr_weaval)

        #Set current temp
        Pg6_C1_temp = tempDetermine(Pg6_C1_curr_weaval)
        Pg6_C2_temp = tempDetermine(Pg6_C2_curr_weaval)
        Pg6_C3_temp = tempDetermine(Pg6_C3_curr_weaval)
        Pg6_C4_temp = tempDetermine(Pg6_C4_curr_weaval)
        Pg6_C5_temp = tempDetermine(Pg6_C5_curr_weaval)
        Pg6_C6_temp = tempDetermine(Pg6_C6_curr_weaval)
        Pg6_C7_temp = tempDetermine(Pg6_C7_curr_weaval)
        # Manitoba and Regional Temperatures & Conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
        X_VAL = 0
        # create 8 lines of text   
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg6_C1_Name + "," + Pg6_C1_State + "   " + Pg6_C1_temp + " F" + " " + Pg6_C1_shortForcast)
        s3=(Pg6_C2_Name + "," + Pg6_C2_State + " " + Pg6_C2_temp + " F" + " " + Pg6_C2_shortForcast)
        s4=(Pg6_C3_Name + "," + Pg6_C3_State + " " + Pg6_C3_temp + " F" + " " + Pg6_C3_shortForcast)
        s5=(Pg6_C4_Name + "," + Pg6_C4_State + "   " + Pg6_C4_temp + " F" + " " + Pg6_C4_shortForcast)
        s6=(Pg6_C5_Name + "," + Pg6_C5_State + "   " + Pg6_C5_temp + " F" + " " + Pg6_C5_shortForcast)
        s7=(Pg6_C6_Name + "," + Pg6_C6_State + "  " + Pg6_C6_temp + " F" + " " + Pg6_C6_shortForcast)
        s8=(Pg6_C7_Name + "," + Pg6_C7_State + "    " + Pg6_C7_temp + " F" + " " + Pg6_C7_shortForcast)

    elif (PageNum == 7):
    
        # ===================== Screen 7 =====================
         
        Pg7_C1_shortForcast = shortFDetermine(Pg7_C1_curr_weaval)
        Pg7_C2_shortForcast = shortFDetermine(Pg7_C2_curr_weaval)
        Pg7_C3_shortForcast = shortFDetermine(Pg7_C3_curr_weaval)
        Pg7_C4_shortForcast = shortFDetermine(Pg7_C4_curr_weaval)
        Pg7_C5_shortForcast = shortFDetermine(Pg7_C5_curr_weaval)
        Pg7_C6_shortForcast = shortFDetermine(Pg7_C6_curr_weaval)
        Pg7_C7_shortForcast = shortFDetermine(Pg7_C7_curr_weaval)

        Pg7_C1_temp = tempDetermine(Pg7_C1_curr_weaval)
        Pg7_C2_temp = tempDetermine(Pg7_C2_curr_weaval)
        Pg7_C3_temp = tempDetermine(Pg7_C3_curr_weaval)
        Pg7_C4_temp = tempDetermine(Pg7_C4_curr_weaval)
        Pg7_C5_temp = tempDetermine(Pg7_C5_curr_weaval)
        Pg7_C6_temp = tempDetermine(Pg7_C6_curr_weaval)
        Pg7_C7_temp = tempDetermine(Pg7_C7_curr_weaval)


        # Western Canada Temperatures & Conditions       
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
        X_VAL = 0
        # create 8 lines of text     
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg7_C1_Name + "," + Pg7_C1_State + "        " + Pg7_C1_temp + " F" + " " + Pg7_C1_shortForcast)
        s3=(Pg7_C2_Name + "," + Pg7_C2_State + "      " + Pg7_C2_temp + " F" + " " + Pg7_C2_shortForcast)
        s4=(Pg7_C3_Name + "," + Pg7_C3_State + "    " + Pg7_C3_temp + " F" + " " + Pg7_C3_shortForcast)
        s5=(Pg7_C4_Name + "," + Pg7_C4_State + "       " + Pg7_C4_temp + " F" + " " + Pg7_C4_shortForcast)
        s6=(Pg7_C5_Name + "," + Pg7_C5_State + "    " + Pg7_C5_temp + " F" + " " + Pg7_C5_shortForcast)
        s7=(Pg7_C6_Name + "," + Pg7_C6_State + "   " + Pg7_C6_temp + " F" + " " + Pg7_C6_shortForcast)
        s8=(Pg7_C7_Name + "  " + Pg7_C7_temp + " F" + " " + Pg7_C7_shortForcast)
             
    elif (PageNum == 8):   
    
        # ===================== Screen 8 =====================
        #Set current short forcast
        Pg8_C1_shortForcast = shortFDetermine(Pg8_C1_curr_weaval)
        Pg8_C2_shortForcast = shortFDetermine(Pg8_C2_curr_weaval)
        Pg8_C3_shortForcast = shortFDetermine(Pg8_C3_curr_weaval)
        Pg8_C4_shortForcast = shortFDetermine(Pg8_C4_curr_weaval)
        Pg8_C5_shortForcast = shortFDetermine(Pg8_C5_curr_weaval)
        Pg8_C6_shortForcast = shortFDetermine(Pg8_C6_curr_weaval)
        Pg8_C7_shortForcast = shortFDetermine(Pg8_C7_curr_weaval)

        #Set current temp
        Pg8_C1_temp = tempDetermine(Pg8_C1_curr_weaval)
        Pg8_C2_temp = tempDetermine(Pg8_C2_curr_weaval)
        Pg8_C3_temp = tempDetermine(Pg8_C3_curr_weaval)
        Pg8_C4_temp = tempDetermine(Pg8_C4_curr_weaval)
        Pg8_C5_temp = tempDetermine(Pg8_C5_curr_weaval)
        Pg8_C6_temp = tempDetermine(Pg8_C6_curr_weaval)
        Pg8_C7_temp = tempDetermine(Pg8_C7_curr_weaval)
        # Eastern Canada Temperatures & Conditions       
        PageNum = PageNum + 1
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
        X_VAL = 0
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg8_C1_Name + "," + Pg8_C1_State + " " + Pg8_C1_temp + " F" + " " + Pg8_C1_shortForcast)
        s3=(Pg8_C2_Name + "," + Pg8_C2_State + "         " + Pg8_C2_temp + " F" + " " + Pg8_C2_shortForcast)
        s4=(Pg8_C3_Name + "," + Pg8_C3_State + "       " + Pg8_C3_temp + " F" + " " + Pg8_C3_shortForcast)
        s5=(Pg8_C4_Name + "," + Pg8_C4_State + "        " + Pg8_C4_temp + " F" + " " + Pg8_C4_shortForcast)
        s6=(Pg8_C5_Name + "," + Pg8_C5_State + "     " + Pg8_C5_temp + " F" + " " + Pg8_C5_shortForcast)
        s7=(Pg8_C6_Name + "," + Pg8_C6_State + "        " + Pg8_C6_temp + " F" + " " + Pg8_C6_shortForcast)
        s8=(Pg8_C7_Name + "," + Pg8_C7_State + "     " + Pg8_C7_temp + " F" + " " + Pg8_C7_shortForcast)
    
    elif (PageNum == 9):
        
        # ===================== Screen 9 =====================
      

        # hourly forecast
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
    
        # get local timezone to show on screen
        local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        hrly_period_local = list(map(lambda x: x.astimezone(), hrly_period))
        X_VAL = 80
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
        Pg6_C1_precip = precipDetermine(Pg6_C1_curr_weaval)
        Pg6_C3_precip = precipDetermine(Pg6_C3_curr_weaval)
        Pg6_C6_precip = precipDetermine(Pg6_C6_curr_weaval)
        Pg7_C5_precip = precipDetermine(Pg7_C5_curr_weaval)
        Pg7_C7_precip = precipDetermine(Pg7_C7_curr_weaval)
        Pg8_C2_precip = precipDetermine(Pg8_C2_curr_weaval)
        Pg8_C7_precip = precipDetermine(Pg8_C7_curr_weaval)
        # preciptation page
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)        
        X_VAL = 80
        # create 8 lines of text   
        s1 = ("CURRENT PRECIPITATION FORECAST").center(35," ")
        s2 =("          " + Pg6_C1_Name + "," + Pg6_C1_State + "       " + Pg6_C1_precip + " %")
        s3 =("          " + Pg6_C3_Name + "," + Pg6_C3_State + "     " + Pg6_C3_precip + " %")
        s4 =("          " + Pg6_C6_Name + "," + Pg6_C6_State + "      " + Pg6_C6_precip + " %")
        s5 =("          " + Pg7_C5_Name + "," + Pg7_C5_State + "    " + Pg7_C5_precip + " %")
        s6 =("          " + Pg7_C7_Name + "  " + Pg7_C7_precip + " %")
        s7 =("          " + Pg8_C2_Name + "," + Pg8_C2_State + "      " + Pg8_C2_precip + " %")
        s8 =("          " + Pg8_C7_Name + "," + Pg8_C7_State + "  " + Pg8_C7_precip + " %")

    elif (PageNum == 11):    
        
        # ===================== Screen 11 =====================
        # custom/extra page - currently used for my channel listing
        # to disable this page, set PageTotal to 10
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)         
      
        # create 8 lines of text
        X_VAL = 80
        s1 = "MESSAGE FROM TECHSAVVVVY"
        s2 = "I hope you enjoy my version of"    
        s3 = "probnot's Retro Weather Channel." 
        s4 = "This was modifed with permission"         
        s5 = "from probnot's video on 12/4/22."
        s6 = "You may also adapt my version in any"
        s7 = "way you wish, enjoy!"
        s8 = "-TechSavvvvy" 

    # create the canvas for middle page text

    weather = Canvas(root, height=310, width=720, bg=PageColour)
    weather.place(x=0, y=85)
    weather.config(highlightbackground=PageColour)
    
    # place the 8 lines of text
    weather.create_text(X_VAL, 17, anchor='nw', text=s1, font=('VCR OSD Mono', 21, "bold"), fill="white")
    weather.create_text(X_VAL, 60, anchor='nw', text=s2, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(X_VAL, 95, anchor='nw', text=s3, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(X_VAL, 130, anchor='nw', text=s4, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(X_VAL, 165, anchor='nw', text=s5, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(X_VAL, 200, anchor='nw', text=s6, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(X_VAL, 235, anchor='nw', text=s7, font=('VCR OSD Mono', 21,), fill="white") 
    weather.create_text(X_VAL, 270, anchor='nw', text=s8, font=('VCR OSD Mono', 21,), fill="white") 
    
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
if Music == ON: #Added by TechSavvvvy to allow music player to be easily enabled/disabled
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
else:
 print("Music player has been disabled")
# DEF play background music
if Music == ON: #Added by TechSavvvvy to allow music player to be easily enabled/disabled
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
else:
 print("Music player has been disabled")
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
Title = Label(root, text="ENVIORNMENT USA", font=("VCR OSD Mono", 22, "bold"), fg="white", bg="green")
Title.place(x=0, y=40)

# total number of groups broken up to update sections of weather data, to keep update time short
grouptotal = 3 

# Middle Section (Cycling weather pages, every 30sec)
debug_msg("ROOT-launching weather_page",1)
PageColour = "blue" # blue
PageNum = 1
weather_page(PageColour, PageNum)
if Music == ON: #Added by TechSavvvvy to allow music player to be easily enabled/disabled
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
else:
 print("Music player has been disabled")
# Bottom Scrolling Text (City of Winnipeg RSS Feed)
debug_msg("ROOT-launching bottom_marquee",1)
bottom_marquee(grouptotal)

# loop program  
root.mainloop()

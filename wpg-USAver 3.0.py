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
import sys
prog = "wpg-usa"
ver = "3.0"
Music = ON #Enables or disables music player, ON to turn it on, and anyhing else to disable it
#probnot's Retro Winnipeg Weather Channel USA version by TechSavvvvy
#Started on June 27, 2024, last updated August 6, 2024

#Change log

#V3.0
    #Fixed mispelling of forecast, was forcast before.
    #Removed previous change log entries to save space, will be in a dedicated file on GitHub
    #Removed env_canda error from RSS feed updater (I usually didn't run the program long enough to get it, lol)
    #Fixed issue with rainPoss where 80% or above would cause the program to crash due to an incorrect </> sign, also added else statement to prevent future crashing
    #Changed screen routine debug messages to 3 priorty
    #Converted previous print messages used for troubleshooting updater to debug messages with a 2 priority
    #Added diagnostic priority to probnot's debug message function
ZIP = 97035 #Enter USA ZIP code here, added by -TS, TX-75007 Kill Devil Hills 27948
Pg1_City = "PORTLAND"


Pg6_C1_Name = "DETRIOT" #Set city name for the first city on page 6, used only for looks
Pg6_C1_State = "MI" #Set 2 digit state abbreviation for first city on page 6, also only used for looks
Pg6_C1_Zip = 48127 #Zip code for first city on page 6, used by NOAA to determine weather data

# From here on it repeats itself
Pg6_C2_Name = "CAVE CITY" ; Pg6_C2_State = "KY" ; Pg6_C2_Zip = 42127
Pg6_C3_Name = "N.Y. CITY"; Pg6_C3_State = "NY"; Pg6_C3_Zip = 10001
Pg6_C4_Name = "SEATTLE"; Pg6_C4_State = "WA"; Pg6_C4_Zip = 98039
Pg6_C5_Name = "CHICAGO"; Pg6_C5_State = "IL" ;Pg6_C5_Zip = 60007
Pg6_C6_Name = "MARIETTA" ; Pg6_C6_State = "OH" ; Pg6_C6_Zip = 47750
Pg6_C7_Name = "TOLEDO" ; Pg6_C7_State = "OH" ; Pg6_C7_Zip = 43537

Pg7_C1_Name = "AUSTIN" ; Pg7_C1_State = "TX" ;Pg7_C1_Zip = 77301
Pg7_C2_Name = "COLUMBUS" ; Pg7_C2_State = "OH" ;Pg7_C2_Zip = 43004
Pg7_C3_Name = "MONTGOMERY" ; Pg7_C3_State = "AL" ; Pg7_C3_Zip = 36043
Pg7_C4_Name = "RALEIGH" ; Pg7_C4_State = "NC" ; Pg7_C4_Zip = 27513
Pg7_C5_Name = "SACRAMENTO" ; Pg7_C5_State = "CA" ; Pg7_C5_Zip = 95758
Pg7_C6_Name = "TALLAHASSEE" ; Pg7_C6_State = "FL" ; Pg7_C6_Zip = 32301
Pg7_C7_Name = "WASHINGTON D.C." ; Pg7_C7_State = " " ; Pg7_C7_Zip = 20500

Pg8_C1_Name = "KILL DEVIL HILLS" ; Pg8_C1_State = "NC" ; Pg8_C1_Zip = 27948
Pg8_C2_Name = "HONOLULU" ; Pg8_C2_State = "HI" ; Pg8_C2_Zip = 96795
Pg8_C3_Name = "LA ANGELES" ; Pg8_C3_State = "CA" ; Pg8_C3_Zip = 90001
Pg8_C4_Name = "LAS VEGAS" ; Pg8_C4_State = "NV" ; Pg8_C4_Zip = 89166
Pg8_C5_Name = "MYRTLE BEACH" ; Pg8_C5_State = "SC" ; Pg8_C5_Zip = 29572
Pg8_C6_Name = "NAGS HEAD" ; Pg8_C6_State = "NC" ; Pg8_C6_Zip = 27959
Pg8_C7_Name = "NIAGRA FALLS" ; Pg8_C7_State = "NY" ; Pg8_C7_Zip = 14301

root = Tk()
root.attributes('-fullscreen',False)
root.geometry("720x480") # this must be 720x480 for a proper filled out screen on composite output. 640x480 will have black bar on RH side. use 720x576 for PAL.
root.config(cursor="none", bg="green")
root.wm_title("The Weather Channel")
updateTimer = 1800000 #30 minutes
current_time = datetime.datetime.now()

# DEF debug messenger
def debug_msg(message, priority): #Written by probnot, moved to the top so it would work earlier

    debugmode = 1;
    # 0 = disabled
    # 1 = normal (priority 1)
    # 2 = dignostic (Added by TechSavvvvy)
    # 3 = verbose (priority 3)
    
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

def shortFDetermine(FDetIn): #Used to determine forecast, called by pages 1-3, 6-8 (4 and 5 are currently disabled)
     dirtyIn = FDetIn[450:580]
     if 'Mostly Clear' in dirtyIn: #dirtyIn will contain the forecast, and other garbage info, this is used to remove the garbage info
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
        debug_msg(("General Rain forecast used for" + dirtyIn),2)
        return "RAIN" #Used as general catch all for anything with rain
     elif 'Storm' in dirtyIn:
        debug_msg(("General Storm forecast used for" + dirtyIn),2)
        return "STORM" #Used as general catch all for anything with rain
     elif 'Slight Chance Showers' in dirtyIn:
        return "POSSIBLE RAIN"
     elif 'Shower' in dirtyIn:
        debug_msg(("General Shower forecast used for" + dirtyIn),2)
        return "RAIN"
     else:
        debug_msg(("Unknown Forecast" + dirtyIn),1)
        return "ERROR"

def tempDetermine(dirty_TempIn):
        tempDirty = (dirty_TempIn[140:150]) #Isloates a section of the long string of data from NOAA, temp value will be surrounded by garbage data
        tempClean = re.sub("\\D", "", tempDirty) #Pulls only numbers from data, so in theory only the temp value will be left
        return tempClean

def precipDetermine(dirty_precipIn): #Works similar to tempDetermine
        precipDirty = (dirty_precipIn[255:275])
        precipClean = re.sub("\\D", "", precipDirty)
        return precipClean

#Set current humidity. Works similar to tempDetermine function.
def humidDetermine(humidIn):
    humidDirty = (humidIn[355:405])
    humidNums = re.sub("\\D", "", humidDirty)
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
    WindStr = re.sub("\\D", "", WindSpdDirty)
    Windint = WindStr
    if Windint.isdigit(): #Checks if Windit is a number, if there's no wind there will be no value
         return str(Windint)
    else:
        return str(0) #Replaces empty value with 0 if necessary

def dewDetermine(dewIn):
    dewDirty = (dewIn[310:345]) #Pull section from current weather info
    dewRaw = re.sub("\\D", "", dewDirty) #Pull numbers from section
    dewC = (dewRaw[0:2]) + "." + (dewRaw[3:5]) #Pull only 4 digits in form xx.xx. This is in celcius
    dewC_S = float(dewC) #Convert string (dewC) to float data type 
    dewF = (dewC_S * 1.8) + 32 #Convert C to F
    dewF_S = str(dewF) #Convert F value to string
    dewOut = (dewF_S[0:4]) #Finalize value by removing extra numbers from result
    return dewOut

def pressureDetermine(pressureIn):
    pressureDirty = (pressureIn[950:1050]) #Works similar to setting current temp
    pressureNum = re.sub("\\D", "", pressureDirty)
    PressureOut = (pressureNum[0:3] + "." + pressureNum[4:5]) #Puts pressure in xxx.x format
    return PressureOut

def visDetermine(visIn):
    visDirty = (visIn[1100:1200]) #Works similar to setting current temp
    visNum = re.sub("\\D", "", visDirty)
    VisibilityOut = (visNum[0:2]) #Pulls only first 2 digits
    return VisibilityOut

#Set rain possibility
      #Ranges
      # 0-40 Low
      #40.00001-60 Possible
      #60.00001-80 High
      #80+ Very Hih
def rainPossDetermine(rainPossIn):
    precip_int = int(rainPossIn) #Set rain possibility page on precipitation percentage for page 2 forecast
    if precip_int <= 40: #Checks if temp is 40 F or below
           return "LOW" #If 40 or below, LOW possibility
    elif precip_int < 40 >= 60: #Checks if temp is 41-60 F
           return "POSSIBLE" #IF 41-60, POSSIBLE possibility
    elif precip_int < 60 >= 80: #61-80 F
           return "HIGH" #HIGH possibility
    elif precip_int > 80: #80 or above
           return "VERY HIGH" #VERY HIGH possibility
    else:
           return "ERROR" #In case none of the above applies (which shouldn't happen, but things go wrong) it will show error instead of crashing
#Set general temp
       #Temp ranges
       #Less than 40 F Cold
       #41-60 F Cool
       #61-70 F Warm
       #71+ F Hot
def shortTempDetermine(tempIn):
    temp_int = int(tempIn) #Sets general/short temp for page two forecast using different ranges of temperature
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
def weekData(): #This is used to setup data used on page 3, this was tricky to figure out. All data is stored in a text file in /tmp and read back using linecache, allowing each line of text to be imported as a variable
    WeeklyData = open("/tmp/weekData.txt", "w") #Creates file to be written to, overwrites if it already exists
    sys.stdout = WeeklyData #Changes standard out of console (what you see in the terminal window when the progrma outputs text) to go to the text file instead
    n = NOAA() #Same thing as pullData
    res = n.get_forecasts(ZIP, 'US')
    for i in res:
        print(i) #Prints data to stdout, which has been redirected to a text file
    sys.stdout = sys.__stdout__ #Changes stdout back to normal
def pullWeatherData(): #Obtaining weather data from NWS/NOAA
#Get page 1 and 2 weather data
    debug_msg("Getting Page 1 and 2 Weather Data",1)
    global curr_weaval #Export all variables to outside of function. Without this nothing outside of this function will be able to access the variables, which would make the program unusable
    global Pg6_C1_curr_weaval
    global Pg6_C2_curr_weaval
    global Pg6_C3_curr_weaval
    global Pg6_C4_curr_weaval
    global Pg6_C5_curr_weaval
    global Pg6_C6_curr_weaval
    global Pg6_C7_curr_weaval
    global Pg7_C1_curr_weaval
    global Pg7_C2_curr_weaval
    global Pg7_C3_curr_weaval
    global Pg7_C4_curr_weaval
    global Pg7_C5_curr_weaval
    global Pg7_C6_curr_weaval
    global Pg7_C7_curr_weaval
    global Pg8_C1_curr_weaval
    global Pg8_C2_curr_weaval
    global Pg8_C3_curr_weaval
    global Pg8_C4_curr_weaval
    global Pg8_C5_curr_weaval
    global Pg8_C6_curr_weaval
    global Pg8_C7_curr_weaval
    curr_weaval = pullData(ZIP) #Setup page 1 data using pullData function
    weekData() #Setup page 3 data using weekData function
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
pullWeatherData()
def weatherDataUpdate(): #Obtaining weather data from NWS/NOAA
#Get page 1 and 2 weather data
    global UpdateHour
    global updateTimer
    global current_time
#Set weather data for pages 6-8
    current_time = datetime.datetime.now()
    if current_time.hour == UpdateHour:
     updateTimer = 10000
     if startUpdate == 1:
       pullWeatherData()
       updateHour() 
       updateTimer = 600000 # 1800000 #30 minutes
       pg1DateTimeUpdate()
       T_Date = dateBuild()
       Today_Data_Dirty = extraData()
     else:
       debug_msg("Update ready, waiting for correct page.",2)
    else:
      debug_msg("Update not needed yet!",2)
    root.after(updateTimer, weatherDataUpdate)

def monthSet():
    #Set current date/time
    #This outputs the month as a number, 1 being January and 12 being December, the if/elif is used to translate the number to a shortened verison of the name
    if current_time.month == 1:
          return "JAN"
    elif current_time.month == 2:
          return "FEB"
    elif current_time.month == 3:
         return "MAR"
    elif current_time.month == 4:
          return "APR"
    elif current_time.month == 5:
          return "MAY"
    elif current_time.month == 6:
          return "JUN"
    elif current_time.month == 7:
          return "JUL"
    elif current_time.month == 8:
          return "AUG"
    elif current_time.month == 9:
          return "SEP"
    elif current_time.month == 10:
          return "OCT"
    elif current_time.month == 11:
          return "NOV"
    elif current_time.month == 12:
          return "DEC"
    else:
          return "ERR"

#Determine Hour and AM/PM
def pg1TimeSet():
    current_time = datetime.datetime.now()
    debug_msg("Updating Hour",2)
    global Hour
    global AM_PM
    if current_time.hour > 12: #current_time.hour is in 24 hour/military time, this line detects if it's past 12:00 PM (not AM)
         Hour = current_time.hour - 12 #Subtracts 12 from hour if it's after 12, converting from military time to AM/PM time
         AM_PM = "PM" #Tells program to show PM on page 1
    elif current_time.hour == 0: # Detects if time is 12:00 AM
         Hour = 12 #Sets Hour variable to 12
         AM_PM = "AM" #Tells program to show AM on page 1
    elif current_time.hour < 12: # Detects if time is befrom 12:00 pm
         Hour = current_time.hour #Sets Hour variable to current hour, no math is needed
         AM_PM = "AM" #Tells program to show AM on page 1
    elif current_time.hour == 12: # Detects if time is 12:00 pm
         Hour = current_time.hour #Sets Hour variable to current hour, no math is needed
         AM_PM = "PM" #Tells program to show PM on page 1
    else:
         Hour = "ER" #Failure message in case something goes wrong, this should never happen

#Determine Weekday
def pg1DaySet():
    if current_time.weekday() == 0: #Determines day of week, this is similar to the way month is determined, 0 is Monday and 6 is Sunday
         return "MON"
    elif current_time.weekday() == 1:
         return "TUE"
    elif current_time.weekday() == 2:
         return "WED"
    elif current_time.weekday() == 3:
         return "THU"
    elif current_time.weekday() == 4:
         return "FRI"
    elif current_time.weekday() == 5:
         return "SAT"
    elif current_time.weekday() == 6:
         return "SUN"
    else:
         Day = "ERR"

#Set current Date
def pg1DateSet():
    Date_String = str(current_time.day) #Find currrent date, just the date itself. In other words, it's not determining "07-20-2024", it would determine that it's the 20th
    if current_time.day < 10: #Detects if it's before the 10th
         return ("0" + Date_String) #If it's before the 10th, a "0" will be added in front of it, ex. changing 8 to 08. Used for NOAA and looks. 
    else:
        return Date_String
def pg1DateTimeUpdate(): #This updates the time and date on page 1
    debug_msg("Updating pg 1 time/date",1)
    global Day #Make variables global, so they will be passed to the rest of the program
    global Date
    global Month
    global Year_String
    global Hour_String
    Month = monthSet() #Call various functions to update data
    pg1TimeSet()
    Day = pg1DaySet()
    Date = pg1DateSet()
    Year_String = str(current_time.year)
    Hour_String = str(Hour)
pg1DateTimeUpdate() #Calls above function, only used when the program first runs, after which it's called by weatherDataUpdate

#Build current date in YYYY-MM-DD form to obtain more data from NOOAA
def dateBuild():
    Month_Str = str(current_time.month) #Month value needs to be in string form for this to work
    if current_time.month < 10: #Determines if month is a 1 digit value
        Month_Num = ("0" + Month_Str) #Adds 0 in front of month value, ex. instead of January being 1, it would be 01. Needed for NOAA
    else:
        Month_Num = Month_Str #ignores above for months with 2 digit value
    return (Year_String + "-" + Month_Num + "-" + Date) #Builds data value in YYYY-MM-DD form
T_Date = dateBuild() #Calls above function, only used when the program first runs, after which it's called by weatherDataUpdate

#Get extra forecast data, this is needed for Pressure and visibility
def extraData():
    n = NOAA()
    observations = n.get_observations(ZIP,'US',start=T_Date,end=T_Date)
    for Today_Data in observations:
        return str(Today_Data)
        break
Today_Data_Dirty = extraData() #This is being updated by weatherDataUpdate
#Set Time Zone
TZ = time.tzname
TZ_String = str(TZ)
def updateHour(): #Determines what the UpdateHour variable needs to be, which is used to determine when data needs to be updated
    global UpdateHour
    UpdateHour = current_time.hour + 1 #Sets UpdateHour by taking current hour and adding one
    if UpdateHour == 24: #If the time is 11pm when the progrm is run, it will be 23:00, adding an hour would be 24:00, however, midnight is actually 0:00, therefore the program would never update
        UpdateHour = 0 #This makes it 0 if needed, which is only at 11pm, so it will update after midnight
    else:
        UpdateHour = UpdateHour
updateHour()
#Shared data
temp = tempDetermine(curr_weaval)
WindDir = WinDirDetermine(curr_weaval)
WindSpd = WindSpdDetermine(curr_weaval)
humid = humidDetermine(curr_weaval)
precip = precipDetermine(curr_weaval)
shortForecast = shortFDetermine(curr_weaval)
PageNum = " "
startUpdate = " "
debug_msg("Launching Screen Routine",1) #Used to send message to CLI that the screen routine will begin, also let's you know all weather data has been successfully obtained
debug_msg(("Current Hour is: " + str(current_time.hour)),2)
debug_msg(("Update Hour is: " + str(UpdateHour)),2)
def weather_page(PageColour, PageNum): #Written by probnot
    # pull in current seconds and minutes -- to be used to cycle the middle section every 30sec
#    global PageNum
    time_sec = time.localtime().tm_sec
    time_min = time.localtime().tm_min
    
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    months = [" ", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]    
    linebreak = ['\n']

    PageTotal = 11
    if (PageNum == 1):
        # ===================== Screen 1 =====================
       # PageNum = PageNum + 7 #remove to bring back page 2
        dew = dewDetermine(curr_weaval)
        Pressure = pressureDetermine(Today_Data_Dirty)
        Visibility = visDetermine(Today_Data_Dirty)
        # Today's day/date + specific weather conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3)             
        X_VAL = 80
        # create 8 lines of text     
        s1 = (" " + Pg1_City + " " + Hour_String + " " + AM_PM + " " + (TZ_String[9:12]) + "  " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2 = ("TEMP  " + temp + " F" + "            WIND " + WindDir + " " + WindSpd + " MPH") #Fixed
        # s2 = s2[0:24] + " HIGH " + "?" + " F" Removed due to NOAA not showing High temp
        s3 = shortForecast + "                         " #Fixed
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
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3) 
       # PageNum = PageNum +3 #Added by TS to skip forecast continued pages, comment out or remove this line to bring them back
        X_VAL = 80
        s1 = ("        " + Pg1_City + " CITY FORECAST")
        s2 = ("TODAY'S WEATHER WILL BE " + shortForecast + ".")
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
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3) 
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

        filename = '/tmp/weekData.txt'
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
        s2 = ("TODAY      " + temp + " F " + "Rain: " + precip + "% " + shortForecast)
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
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3)            
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
        
        #Set current short forecast
        Pg6_C1_shortForecast = shortFDetermine(Pg6_C1_curr_weaval)
        Pg6_C2_shortForecast = shortFDetermine(Pg6_C2_curr_weaval)
        Pg6_C3_shortForecast = shortFDetermine(Pg6_C3_curr_weaval)
        Pg6_C4_shortForecast = shortFDetermine(Pg6_C4_curr_weaval)
        Pg6_C5_shortForecast = shortFDetermine(Pg6_C5_curr_weaval)
        Pg6_C6_shortForecast = shortFDetermine(Pg6_C6_curr_weaval)
        Pg6_C7_shortForecast = shortFDetermine(Pg6_C7_curr_weaval)

        #Set current temp
        Pg6_C1_temp = tempDetermine(Pg6_C1_curr_weaval)
        Pg6_C2_temp = tempDetermine(Pg6_C2_curr_weaval)
        Pg6_C3_temp = tempDetermine(Pg6_C3_curr_weaval)
        Pg6_C4_temp = tempDetermine(Pg6_C4_curr_weaval)
        Pg6_C5_temp = tempDetermine(Pg6_C5_curr_weaval)
        Pg6_C6_temp = tempDetermine(Pg6_C6_curr_weaval)
        Pg6_C7_temp = tempDetermine(Pg6_C7_curr_weaval)
        # Manitoba and Regional Temperatures & Conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3)
        X_VAL = 0
        # create 8 lines of text   
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg6_C1_Name + "," + Pg6_C1_State + "   " + Pg6_C1_temp + " F" + " " + Pg6_C1_shortForecast)
        s3=(Pg6_C2_Name + "," + Pg6_C2_State + " " + Pg6_C2_temp + " F" + " " + Pg6_C2_shortForecast)
        s4=(Pg6_C3_Name + "," + Pg6_C3_State + " " + Pg6_C3_temp + " F" + " " + Pg6_C3_shortForecast)
        s5=(Pg6_C4_Name + "," + Pg6_C4_State + "   " + Pg6_C4_temp + " F" + " " + Pg6_C4_shortForecast)
        s6=(Pg6_C5_Name + "," + Pg6_C5_State + "   " + Pg6_C5_temp + " F" + " " + Pg6_C5_shortForecast)
        s7=(Pg6_C6_Name + "," + Pg6_C6_State + "  " + Pg6_C6_temp + " F" + " " + Pg6_C6_shortForecast)
        s8=(Pg6_C7_Name + "," + Pg6_C7_State + "    " + Pg6_C7_temp + " F" + " " + Pg6_C7_shortForecast)

    elif (PageNum == 7):
    
        # ===================== Screen 7 =====================
         
        Pg7_C1_shortForecast = shortFDetermine(Pg7_C1_curr_weaval)
        Pg7_C2_shortForecast = shortFDetermine(Pg7_C2_curr_weaval)
        Pg7_C3_shortForecast = shortFDetermine(Pg7_C3_curr_weaval)
        Pg7_C4_shortForecast = shortFDetermine(Pg7_C4_curr_weaval)
        Pg7_C5_shortForecast = shortFDetermine(Pg7_C5_curr_weaval)
        Pg7_C6_shortForecast = shortFDetermine(Pg7_C6_curr_weaval)
        Pg7_C7_shortForecast = shortFDetermine(Pg7_C7_curr_weaval)

        Pg7_C1_temp = tempDetermine(Pg7_C1_curr_weaval)
        Pg7_C2_temp = tempDetermine(Pg7_C2_curr_weaval)
        Pg7_C3_temp = tempDetermine(Pg7_C3_curr_weaval)
        Pg7_C4_temp = tempDetermine(Pg7_C4_curr_weaval)
        Pg7_C5_temp = tempDetermine(Pg7_C5_curr_weaval)
        Pg7_C6_temp = tempDetermine(Pg7_C6_curr_weaval)
        Pg7_C7_temp = tempDetermine(Pg7_C7_curr_weaval)


        # Western Canada Temperatures & Conditions       
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3) 
        X_VAL = 0
        # create 8 lines of text     
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg7_C1_Name + "," + Pg7_C1_State + "        " + Pg7_C1_temp + " F" + " " + Pg7_C1_shortForecast)
        s3=(Pg7_C2_Name + "," + Pg7_C2_State + "      " + Pg7_C2_temp + " F" + " " + Pg7_C2_shortForecast)
        s4=(Pg7_C3_Name + "," + Pg7_C3_State + "    " + Pg7_C3_temp + " F" + " " + Pg7_C3_shortForecast)
        s5=(Pg7_C4_Name + "," + Pg7_C4_State + "       " + Pg7_C4_temp + " F" + " " + Pg7_C4_shortForecast)
        s6=(Pg7_C5_Name + "," + Pg7_C5_State + "    " + Pg7_C5_temp + " F" + " " + Pg7_C5_shortForecast)
        s7=(Pg7_C6_Name + "," + Pg7_C6_State + "   " + Pg7_C6_temp + " F" + " " + Pg7_C6_shortForecast)
        s8=(Pg7_C7_Name + "  " + Pg7_C7_temp + " F" + " " + Pg7_C7_shortForecast)
             
    elif (PageNum == 8):   
    
        # ===================== Screen 8 =====================
        #Set current short forecast
        Pg8_C1_shortForecast = shortFDetermine(Pg8_C1_curr_weaval)
        Pg8_C2_shortForecast = shortFDetermine(Pg8_C2_curr_weaval)
        Pg8_C3_shortForecast = shortFDetermine(Pg8_C3_curr_weaval)
        Pg8_C4_shortForecast = shortFDetermine(Pg8_C4_curr_weaval)
        Pg8_C5_shortForecast = shortFDetermine(Pg8_C5_curr_weaval)
        Pg8_C6_shortForecast = shortFDetermine(Pg8_C6_curr_weaval)
        Pg8_C7_shortForecast = shortFDetermine(Pg8_C7_curr_weaval)

        #Set current temp
        Pg8_C1_temp = tempDetermine(Pg8_C1_curr_weaval)
        Pg8_C2_temp = tempDetermine(Pg8_C2_curr_weaval)
        Pg8_C3_temp = tempDetermine(Pg8_C3_curr_weaval)
        Pg8_C4_temp = tempDetermine(Pg8_C4_curr_weaval)
        Pg8_C5_temp = tempDetermine(Pg8_C5_curr_weaval)
        Pg8_C6_temp = tempDetermine(Pg8_C6_curr_weaval)
        Pg8_C7_temp = tempDetermine(Pg8_C7_curr_weaval)
        # Eastern Canada Temperatures & Conditions       
        if current_time.hour == UpdateHour:
            PageNum = PageNum
        else:
            PageNum = PageNum +1
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3)
        X_VAL = 0
        s1=("          " + Day + " " + Month + " " + Date + "/" + Year_String)
        s2=(Pg8_C1_Name + "," + Pg8_C1_State + " " + Pg8_C1_temp + " F" + " " + Pg8_C1_shortForecast)
        s3=(Pg8_C2_Name + "," + Pg8_C2_State + "         " + Pg8_C2_temp + " F" + " " + Pg8_C2_shortForecast)
        s4=(Pg8_C3_Name + "," + Pg8_C3_State + "       " + Pg8_C3_temp + " F" + " " + Pg8_C3_shortForecast)
        s5=(Pg8_C4_Name + "," + Pg8_C4_State + "        " + Pg8_C4_temp + " F" + " " + Pg8_C4_shortForecast)
        s6=(Pg8_C5_Name + "," + Pg8_C5_State + "     " + Pg8_C5_temp + " F" + " " + Pg8_C5_shortForecast)
        s7=(Pg8_C6_Name + "," + Pg8_C6_State + "        " + Pg8_C6_temp + " F" + " " + Pg8_C6_shortForecast)
        s8=(Pg8_C7_Name + "," + Pg8_C7_State + "     " + Pg8_C7_temp + " F" + " " + Pg8_C7_shortForecast)
    
    elif (PageNum == 9):
        
        # ===================== Screen 9 =====================
        global startUpdate
        # Data updata screen, only displayed when updating weather data
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3)
        # get local timezone to show on screen
        X_VAL = 80
        # create 8 lines of text           
        s1 = "DATA UPDATE IN PROGRESS, PLEASE WAIT"
        s2 = " "
        s3 = " " 
        s4 = " "
        s5 = " "
        s6 = " "
        s7 = " " 
        s8 = " "
        startUpdate = 1
    elif (PageNum == 10):
#        global startUpdate
        startUpdate = 0
        # ===================== Screen 10 =====================
        Pg6_C1_precip = precipDetermine(Pg6_C1_curr_weaval)
        Pg6_C3_precip = precipDetermine(Pg6_C3_curr_weaval)
        Pg6_C6_precip = precipDetermine(Pg6_C6_curr_weaval)
        Pg7_C5_precip = precipDetermine(Pg7_C5_curr_weaval)
        Pg7_C7_precip = precipDetermine(Pg7_C7_curr_weaval)
        Pg8_C2_precip = precipDetermine(Pg8_C2_curr_weaval)
        Pg8_C7_precip = precipDetermine(Pg8_C7_curr_weaval)
        # preciptation page
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3)        
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
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),3)         
      
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

    url = "https://www.kgw.com/feeds/syndication/rss/news"
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
                p = 0 # keep the for loop from ending
                wpg = feedparser.parse(url)
                debug_msg("BOTTOM_MARQUEE-RSS feed refreshed",1)
weatherDataUpdate()
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
Title = Label(root, text=" ⛅ THE WEATHER CHANNEL", font=("VCR OSD Mono", 22, "bold"), fg="white", bg="green")
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
 musicpath = "/home/cmj/mp3/vaporwave/florida rains/Florida Rains/Good Evening Forecast/" # must show full path
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

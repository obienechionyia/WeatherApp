# Weather App! This app will take a country and zip code from the user and return
# a weather report for the area!

# Import modules to be used in program
import requests
from requests import get
import flag
import ipinfo
import json
import datetime
from keys import *

# Key from OpenWeatherMaps API
apiKey = api_key

# Declare global variables to be used in various functions
global locationInput, currentWeather, done, ipAddress
done = True


def getLocation():
    global ipAddress
    # Get user IP address
    ipAddress = get('https://api.ipify.org').text
    # Convert IP address to geolocation data
    geoKey = geo_key
    geoHandler = ipinfo.getHandler(geoKey)
    geoDetails = geoHandler.getDetails(ipAddress)
    return geoDetails.city

# Function to begin the program with a request for user input
def startProgram():
    global currentWeather
    global locationInput
    locationInput = input(
        "Enter a city name, zip code, or 'my location': ").lower()
    # If the user chooses the "my location" option, the getLocation function runs, and retrieves
    # the weather in their current location.
    if locationInput == "my location":
        locationInput = getLocation()
    # If the user enters a zip code, the API link is different than the second link, which is for
    # city names.
    if locationInput.isdigit():
        currentWeather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?zip={locationInput}&units=imperial&appid={apiKey}").json()
    else:
        currentWeather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={locationInput}&units=imperial&appid={apiKey}").json()
    return locationInput

# Function to return the current temperature to the user, in F and C
def currentTemp():
    temperature = currentWeather["main"]["temp"]
    celcius = (temperature - 32) * .5556
    cityName = currentWeather["name"]
    countryCode = currentWeather["sys"]["country"]
    return f"The current temperature in {cityName} {getFlag(countryCode)}  is {int(temperature)}°F({int(celcius)}°C)"

# Function to return the weather status to the user (cloudy, sunny, foggy, etc.)
def weatherMain(getTime):
    skyStatus = currentWeather["weather"][0]["description"]
    skyDict = {"clear": "☀️", "clouds": "☁️", "rain": "🌧️",
               "snow": "❄️", "smoke": "🚬", "fog": "🌫️", "mist": "🌫️"}
    skyDictNight = {"clear": "🌙", "clouds": "☁️", "rain": "🌧️",
                    "snow": "❄️", "smoke": "🚬", "fog": "🌫️", "mist": "🌫️"}
    for i in skyDict:
        if i in skyStatus and (7 < getTime < 19):
            skyStatus = skyStatus + " " + skyDict[i]
    for i in skyDictNight:
        if i in skyStatus and (getTime <= 7 or getTime >= 19):
            skyStatus = skyStatus + " " + skyDictNight[i]
    return f"Current sky status: {skyStatus.title()}"

# Function to return the current wind speed and direction to the user
def windSpeed():
    global done
    speed = currentWeather["wind"]["speed"]
    # Dictionary to hold the directional values, and the direction that the user will be shown based on their location input
    directionDict = {range(0, int(33.75)): "N", range(int(33.76), int(78.75)): "NE", range(int(78.76), int(123.74)): "E",
                     range(int(123.75), int(168.74)): "SE", range(int(168.75), int(213.74)): "S", range(int(213.75), int(258.74)): "SW", range(int(258.75), int(303.74)): "W", range(int(303.75), int(361.00)): "NW"}
    for i in directionDict:
        if currentWeather["wind"]["deg"] in i:
            direction = directionDict[i]
    # If the program runs successfully, the 'done' variable is changed to False, and the main program loop ends as a result
    done = False
    return f"Wind speed: {int(speed)} mph | Wind direction: {direction} 💨"

# Function to retreive the given country's flag emoji
def getFlag(country):
    countryFlag = flag.flag(f"{country}")
    return countryFlag

# Function to get the current time in the user's location input, and change the emojis in the weatherMain function to reflect day/night
def getTime():
    # The offset of the local time from UTC time
    offset = currentWeather["timezone"]
    # UTC time in UNIX time
    utcTime = datetime.datetime.utcnow()
    # Add the local time offset to the UTC time
    localTime = utcTime + datetime.timedelta(seconds=offset)
    # Convert the datetime object to a string of just the hour
    localTimeStr = localTime.strftime("%H")
    # Convert the string to an integer that can be used in the weatherMain function, and return it
    return int(localTimeStr)

while done is True:
    try:
        startProgram()
        print(currentTemp())
        print(weatherMain(getTime()))
        print(windSpeed())
    # If the user doesn't enter a valid city name or zip code, the 'done' variable is not changed to False, and the loop repeats
    except:
        print("Please enter a valid city name or zip code!")

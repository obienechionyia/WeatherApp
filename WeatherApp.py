# Weather App! This app will take a country and zip code from the user and return
# a weather report for the area!

# import modules to be used in program
import requests
from requests import get
import flag
import ipinfo
import json
import datetime
from keys import *

# key from OpenWeatherMaps API
apiKey = api_key

# declare global variables to be used in various functions
global locationInput, currentWeather, done, ipAddress
done = True


def getLocation():
    global ipAddress
    # get user IP address
    ipAddress = get('https://api.ipify.org').text
    # convert IP address to geolocation data
    geoKey = geo_key
    geoHandler = ipinfo.getHandler(geoKey)
    geoDetails = geoHandler.getDetails(ipAddress)
    return geoDetails.city

# function to begin the program with a request for user input


def startProgram():
    global currentWeather
    global locationInput
    locationInput = input(
        "Enter a city name, zip code, or 'my location': ").lower()
    if locationInput == "my location":
        locationInput = getLocation()
    if locationInput.isdigit():
        currentWeather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?zip={locationInput}&units=imperial&appid={apiKey}").json()
    else:
        currentWeather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={locationInput}&units=imperial&appid={apiKey}").json()
    return locationInput

# function to return the current temperature to the user


def currentTemp():
    temperature = currentWeather["main"]["temp"]
    celcius = (temperature - 32) * .5556
    cityName = currentWeather["name"]
    countryCode = currentWeather["sys"]["country"]
    return f"The current temperature in {cityName} {getFlag(countryCode)}  is {int(temperature)}°F({int(celcius)}°C)"

# function to return the main weather status to the user


def weatherMain(getTime):
    skyStatus = currentWeather["weather"][0]["description"]
    skyDict = {"clear": "☀️", "clouds": "☁️", "rain": "🌧️",
               "snow": "❄️", "smoke": "🚬", "fog": "🌫️", "mist": "🌫️"}
    skyDictNight = {"clear": "🌙", "clouds": "☁️", "rain": "🌧️",
                    "snow": "❄️", "smoke": "🚬", "fog": "🌫️", "mist": "🌫️"}
    for i in skyDict:
        # if i in skyStatus and time.time() > currentWeather["sys"]["sunrise"]:
        if i in skyStatus and (7 < getTime < 19):
            skyStatus = skyStatus + " " + skyDict[i]
    for i in skyDictNight:
        # if i in skyStatus and time.time() < currentWeather["sys"]["sunrise"]:
        if i in skyStatus and (getTime <= 7 or getTime >= 19):
            skyStatus = skyStatus + " " + skyDictNight[i]
    return f"Current sky status: {skyStatus.title()}"

# function to return the wind info to the user


def windSpeed():
    global done
    speed = currentWeather["wind"]["speed"]
    directionDict = {range(0, int(33.75)): "N", range(int(33.76), int(78.75)): "NE", range(int(78.76), int(123.74)): "E",
                     range(int(123.75), int(168.74)): "SE", range(int(168.75), int(213.74)): "S", range(int(213.75), int(258.74)): "SW", range(int(258.75), int(303.74)): "W", range(int(303.75), int(361.00)): "NW"}
    for i in directionDict:
        if currentWeather["wind"]["deg"] in i:
            direction = directionDict[i]
    done = False
    return f"Wind speed: {int(speed)} mph | Wind direction: {direction} 💨"

# function to retreive the given country's flag emoji


def getFlag(country):
    countryFlag = flag.flag(f"{country}")
    return countryFlag


def getTime():
    offset = currentWeather["timezone"]
    utcTime = datetime.datetime.utcnow()
    localTime = utcTime + datetime.timedelta(seconds=offset)
    localTimeStr = localTime.strftime("%H")
    return int(localTimeStr)


while done is True:
    try:
        startProgram()
        print(currentTemp())
        print(weatherMain(getTime()))
        print(windSpeed())
    except:
        print("Please enter a valid city name or zip code!")

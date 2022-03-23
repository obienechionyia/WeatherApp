# Weather GUI - This provides a user interface for the weather program, rather than just using the terminal

# Import modules to be used in program
import requests
from requests import get
from keys import *
from tkinter import *
from tkinter import ttk
import ipinfo
import flag
import requests
from requests.structures import CaseInsensitiveDict


# Key from OpenWeatherMaps API
apiKey = api_key

url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"

def getWeather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        currentWeather = result.json()
        cityName = currentWeather["name"]
        country = currentWeather["sys"]["country"]
        temp_f = currentWeather["main"]["temp"]
        temp_c = (temp_f - 32) * .5556
        icon = currentWeather["weather"][0]["icon"]
        weather = currentWeather["weather"][0]["main"]
        country_flag = flag.flag(f"{country}")
        final = (cityName, country, temp_f, temp_c, icon, weather, country_flag)
        return final
    else:
        return None

def search(event):  
    city = city_text.get().lower()
    if city == "my location":
        city = getLocation()
    weather = getWeather(city)
    if weather:
        location_lbl['text'] = "{}, {}".format(weather[0], weather[1]) + " " + weather[6]
        temp_lbl['text'] = '{}°F'.format(round(weather[2]))
        image['bitmap'] = "weather_icons/{}.png".format(weather[4])
        weather_lbl['text'] = '{}'.format(weather[5])
    instructions_lbl.destroy()
    weather_icon.destroy()


def getLocation():
    # Get user IP address
    ipAddress = get('https://api.ipify.org').text
    # Convert IP address to geolocation data
    geoKey = geo_key
    geoHandler = ipinfo.getHandler(geoKey)
    geoDetails = geoHandler.getDetails(ipAddress)
    return geoDetails.city


app = Tk()

app.title("Weather App")
app.geometry("650x250")

app.bind('<Return>', search)

instructions_lbl = Label(app, text="Enter a city name below to see its current weather report!", font=("bold", 25))
instructions_lbl.pack()

weather_icon = Label(app, bitmap="weather_icons/weather.png")
weather_icon.pack()

location_lbl = Label(app, text="", font=("bold", 20))
location_lbl.pack()

image = Label(app, bitmap="")
image.pack()

temp_lbl = Label(app, text="")
temp_lbl.pack()

weather_lbl = Label(app, text="")
weather_lbl.pack()

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text="Search", width=12, command=search)
search_btn.pack()


app.mainloop()



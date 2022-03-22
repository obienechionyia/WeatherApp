# Weather GUI - This provides a user interface for the weather program, rather than just using the terminal

# Import modules to be used in program
import requests
from requests import get
from keys import *
from tkinter import *

# Key from OpenWeatherMaps API
apiKey = api_key

# Declare global variables to be used in various functions
# global currentWeather

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
        final = (cityName, country, temp_f, temp_c, icon, weather)
        return final
    else:
        return None

def search():
    city = city_text.get()
    weather = getWeather(city)
    if weather:
        location_lbl['text'] = "{},{}".format(weather[0], weather[1])
        temp_lbl['text'] = '{}°'.format(weather[2])
        image['bitmap'] = "weather_icons/{}.png".format(weather[4])
        weather_lbl['text'] = '{}'.format(weather[5])


app = Tk()

app.title("Weather App")
app.geometry("700x350")


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
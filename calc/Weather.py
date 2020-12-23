import requests
def weather(w):
    api_key = "ac9ae5f24855de6ba928d40fc22af036"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = w.capitalize()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    r = requests.get(complete_url)
    x = r.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        current_tempc = float(current_temperature) - 273.15 
        return "Temperature (in Celcius) = "+str(current_tempc)+"<br> Atmospheric Pressure (in hPa unit) = "+str(current_pressure)+"<br> Humidity (in percent) = "+str(current_humidity)+"<br> Description = "+str(weather_description)
    else:
        return "City Not Found"
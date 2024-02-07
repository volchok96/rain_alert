import requests
import smtplib

MY_NUMBER = input("Enter your login from SMS.RU: ")
MY_PASSWORD = input("Enter your password  from SMS.RU: ")
MY_CITY = input("Enter your city: ")

weather_api_key = input("Enter your API key from openweathermap.org: ")
weather_api = "https://api.openweathermap.org/data/2.5/forecast"
geo_api_key = input("Enter your API key from opencagedata.com: ")
geo_api = f"https://api.opencagedata.com/geocode/v1/json?q={MY_CITY}&key={geo_api_key}"

result = requests.get(geo_api).json()
lat = float(result["results"][0]["geometry"]["lat"])
lng = float(result["results"][0]["geometry"]["lng"])
weather_parameters = {
    "lat": lat,
    "lon": lng,
    "appid": weather_api_key,
}

response = requests.get(weather_api, params=weather_parameters)
weather_data = response.json()
weather_slice = weather_data["list"][:4]
will_rain = False

for hour_data in weather_slice:
    condition_id = hour_data["weather"][0]["id"]
    if int(condition_id) < 600:
        will_rain = True

if will_rain:
        connection = smtplib.SMTP_SSL("sms.ru", 465)
        connection.login(MY_NUMBER, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_NUMBER,
            to_addrs=MY_NUMBER,
            msg=f"Take an umbrella!"
        )
        connection.quit()
    
        print('Mail successfully sent.')

else:
    print("No rain")
from weatherbit.api import Api
from sense_hat import SenseHat
from datetime import date, datetime
import credentials
import time
import calendar
import sys
from threading import Thread

sense = SenseHat()

e = (0, 0, 0) # empty
o = (255, 128, 0) # orange
w = (200, 200, 200) # white
r = (255, 51, 51) # red
db = (0 ,128, 255) # deep_blue
dg = (96, 96, 96) # deep_grey

api_key = credentials.weatherbit_api_key
api = Api(api_key)
api.set_granularity('daily')
forecast_Rbg = api.get_forecast(city="Regensburg,DE")
forecast_Ingl = api.get_forecast(city="Ingolstadt,DE")

class Display_Weekdays:
    def __init__(self):
        my_date = date.today()
        self.weekday = calendar.day_name[my_date.weekday()]

    def display_weekday_shortcut(self):
        weekday_shortcut = ((self.weekday)[0:3]).upper()
        sense.show_message(weekday_shortcut)

class Get_Weather:
    def __init__(self):
        self.forecast_rbg = forecast_Rbg.get_series(['weather'])
        self.forecast_ingl = forecast_Ingl.get_series(['weather'])
        self.weather_rbg = self.get_forecast()[0]
        self.weather_ingl = self.get_forecast()[1]

    def get_forecast(self):
        weather_rbg = self.forecast_rbg[0]['weather']['description']
        weather_ingl = self.forecast_ingl[0]['weather']['description']
        return weather_rbg, weather_ingl

class Display_Weather:
    def __init__(self):
        self.empty_pet = [
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e,
            e, e, e, e, e, e, e, e
        ]
        self.snow_pet = [
            w, w, e, w, w, e, w, w,
            w, w, e, w, w, e, w, w,
            e, e, w, w, w, w, e, e,
            e, e, e, w, w, e, e, e,
            e, e, e, w, w, e, e, e,
            e, e, w, w, w, w, e, e,
            w, w, e, w, w, e, w, w,
            w, w, e, w, w, e, w, w,
        ]
        self.sunshine_pet_1 = [
            e, e, e, e, o, e, e, e,
            e, e, e, e, o, e, e, e,
            e, e, r, r, r, r, e, e,
            o, o, r, r, r, r, e, e,
            e, e, r, r, r, r, o, o,
            e, e, r, r, r, r, e, e,
            e, e, e, o, e, e, e, e,
            e, e, e, o, e, e, e, e,
        ]
        self.sunshine_pet_2 = [
            o, e, e, o, e, e, e, o,
            e, o, e, o, e, e, o, e,
            e, e, r, r, r, r, e, e,
            e, e, r, r, r, r, o, o,
            o, o, r, r, r, r, e, e,
            e, e, r, r, r, r, e, e,
            e, o, e, e, o, e, o, e,
            o, e, e, e, o, e, e, o,
        ]
        self.rain_pet_1 = [
            e, e, w, w, w, w, w, dg,
            e, w, w, w, w, dg, dg, dg,
            dg, dg, dg, dg, dg, dg, dg, dg,
            e, db, e, db, e, db, e, db,
            e, e, e, e, e, e, e, e,
            e, db, e, db, e, db, e, db,
            e, e, e, e, e, e, e, e,
            e, db, e, db, e, db, e, db
        ]
        self.rain_pet_2 = [
            e, e, w, w, w, w, w, dg,
            e, w, w, w, w, dg, dg, dg,
            dg, dg, dg, dg, dg, dg, dg, dg,
            e, e, e, e, e, e, e, e,
            e, db, e, db, e, db, e, db,
            e, e, e, e, e, e, e, e,
            e, db, e, db, e, db, e, db,
            e, e, e, e, e, e, e, e
        ]
        self.clouds_pet = [
            e, e, e, e, e, e, e, e,
            w, dg, dg, dg, r, r, w, w,
            w, w, w, dg, r, r, dg, dg,
            w, w, w, dg, dg, dg, dg, dg,
            dg, dg, dg, dg, dg, dg, dg, dg,
            w, dg, dg, dg, dg, w, w, w,
            w, w, w, w, w, w, w, w,
            e, e, e, e, e, e, e, e,
        ]

    def display_rain(self):
        for _ in range(2):
            sense.set_pixels(self.rain_pet_1)
            time.sleep(0.5)
            sense.set_pixels(self.rain_pet_2)
            time.sleep(0.5)
        sense.set_pixels(self.empty_pet)

    def display_clouds(self):
        for _ in range(2):
            sense.set_pixels(self.clouds_pet)
            time.sleep(0.5)
            sense.set_pixels(self.empty_pet)
            time.sleep(0.5)
        sense.set_pixels(self.empty_pet)

    def display_sunshine(self):
        for _ in range(2):
            sense.set_pixels(self.sunshine_pet_1)
            time.sleep(0.5)
            sense.set_pixels(self.sunshine_pet_2)
            time.sleep(0.5)
        sense.set_pixels(self.empty_pet)

    def display_snow(self):
        for _ in range(2):
            sense.set_pixels(self.snow_pet)
            time.sleep(1)
            sense.set_pixels(self.empty_pet)
            time.sleep(1)
        sense.set_pixels(self.empty_pet)

    def display_weather(self):
        rain_info = ['rain', 'drizzle', 'sleet']
        snow_ino = ['snow', 'flurries']

        rain_result = [ele for ele in rain_info if(ele in Get_Weather().weather_rbg or ele in Get_Weather().weather_ingl)]
        snow_result = [ele for ele in snow_ino if(ele in Get_Weather().weather_rbg or ele in Get_Weather().weather_ingl)]

        if rain_result:
            self.display_rain()
        elif snow_result:
            self.display_snow()
        elif "Clear" in Get_Weather().weather_rbg or "Clear" in Get_Weather().weather_ingl:
            self.display_sunshine()
        else:
            self.display_clouds()

def output_info():
    start_time = datetime.utcnow()
    while True:
        Display_Weekdays().display_weekday_shortcut()
        Display_Weather().display_weather()
        current_time = datetime.utcnow()
        diff = (current_time - start_time).total_seconds()/60
        mins = 40-int(diff)
        timeformat = '{:02d}'.format(mins)
        sense.show_message(timeformat, text_colour=r, back_colour=w)
        if 40<diff:
            break
    sense.clear()
    return "Output is over"

def main():
    output_info()

if __name__=="__main__":
    main()
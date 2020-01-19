import datetime
import re
import json
import db_notification
from db_notification import Railway_Info
import pytz
from elasticsearch import Elasticsearch

es = Elasticsearch()
today_date = datetime.date.today()

class Basis_Data_From_Schine:

    def is_train_delayed(self, from_station, to_Station, departure_hour, departure_minute, index):
        train_delay_status = False
        info = Railway_Info().get_railway_plan(today_date, departure_hour, departure_minute, from_station, to_Station)
        ontime_info = info[index]["ontime"]
        if False == ontime_info:
            train_delay_status = True
        return train_delay_status

    def get_official_departure(self, from_station, to_Station, departure_hour, departure_minute, index):
        info = Railway_Info().get_railway_plan(today_date, departure_hour, departure_minute, from_station,
                                               to_Station)
        return str(info[index]["departure"])

    def get_official_delayed_time_departure(self, from_station, to_Station, departure_hour, departure_minute, index):
        delay_departure=0
        info = Railway_Info().get_railway_plan(today_date, departure_hour, departure_minute, from_station,
                                               to_Station)
        if False == info[index]["ontime"]:
            delay_departure = info[index]["delay"]["delay_departure"]
        return delay_departure

    def get_official_arrival(self, from_station, to_Station, departure_hour, departure_minute, index):
        info = Railway_Info().get_railway_plan(today_date, departure_hour, departure_minute, from_station,
                                               to_Station)
        return str(info[index]["arrival"])

    def get_official_delayed_time_arrival(self, from_station, to_Station, departure_hour, departure_minute, index):
        delay_arrival = 0
        info = Railway_Info().get_railway_plan(today_date, departure_hour, departure_minute, from_station,
                                               to_Station)
        if False == info[index]["ontime"]:
            delay_arrival = info[index]["delay"]["delay_arrival"]
        return delay_arrival

    def get_official_duration(self, from_station, to_Station, departure_hour, departure_minute, index):
        info = Railway_Info().get_railway_plan(today_date, departure_hour, departure_minute, from_station,
                                               to_Station)
        string_duration = str(info[index]["time"])
        timestamp_duration = datetime.datetime.strptime(string_duration,"%H:%M")
        delta = datetime.timedelta(hours=timestamp_duration.hour, minutes=timestamp_duration.minute, seconds=timestamp_duration.second)
        return delta.seconds #return seconds

    def get_train_info(self, from_station, to_Station, departure_hour, departure_minute, index):
        info = Railway_Info().get_railway_plan(today_date, departure_hour, departure_minute, from_station,
                                               to_Station)
        details = info[index]["products"][0]
        str_departure=str(info[index]["departure"]).split(":")[0]+str(info[index]["departure"]).split(":")[1]
        return str(details+str_departure)


class Basis_Data_From_User:
    def __init__(self):
        self.real_departure_morning = self.get_real_departure_list()[0] # type string
        self.real_departure_afternoon = self.get_real_departure_list()[1] # type string
        self.real_arrival_morning = self.get_real_arrival_list()[0]
        self.real_arrival_afternoon = self.get_real_arrival_list()[1]
        self.morning_train_duration = self.morning_train_duration()
        self.afternoon_train_duration = self.afternoon_train_duration()

    def convert_function(self, results, keyword):
        return_value = []
        for num, doc in enumerate(results):
            for key, value in doc.items():
                if "_source" == key:
                    return_value.append(value[keyword])
        return return_value

    def get_real_departure_list(self):
        with open("/home/dth920312/IoT_Project/record.json", 'r') as load_f:
            data = json.load(load_f)
            departure_morning = data[1][1][1][0]['departure']
            departure_afternoon = data[1][0]['departure']
        return departure_morning, departure_afternoon

    def get_real_arrival_list(self):
        with open("/home/dth920312/IoT_Project/record.json", 'r') as load_f:
            data = json.load(load_f)
            arrival_morning = data[1][1][0]['arrival']
            arrival_afternoon = data[0]['arrival']
        return arrival_morning, arrival_afternoon

    def morning_train_duration(self):
        record_departure_timestamp = datetime.datetime.strptime(self.real_departure_morning, "%H:%M")
        record_arrival_timestamp = datetime.datetime.strptime(self.real_arrival_morning, "%H:%M")
        diff = record_arrival_timestamp - record_departure_timestamp
        return diff.seconds #return seconds

    def afternoon_train_duration(self):
        record_departure_timestamp = datetime.datetime.strptime(self.real_departure_afternoon, "%H:%M")
        record_arrival_timestamp = datetime.datetime.strptime(self.real_arrival_afternoon, "%H:%M")
        diff = record_arrival_timestamp - record_departure_timestamp
        return diff.seconds #return seconds

    def is_morning_train_delayed(self):
        train_delay_status = False

        official_departure = Basis_Data_From_Schine().get_official_departure('Regensburg HbF', 'Ingolstadt Nord', 7, 0, 0)
        official_departure_timestamp = datetime.datetime.strptime(official_departure, "%H:%M")
        official_arrival = Basis_Data_From_Schine().get_official_arrival('Regensburg HbF', 'Ingolstadt Nord', 7, 0, 0)
        official_arrival_timestamp = datetime.datetime.strptime(official_arrival, "%H:%M")

        record_departure_timestamp = datetime.datetime.strptime(self.real_departure_morning, "%H:%M")
        record_arrival_timestamp = datetime.datetime.strptime(self.real_arrival_morning, "%H:%M")

        if official_departure_timestamp != record_departure_timestamp or official_arrival_timestamp != record_arrival_timestamp:
            train_delay_status = True
        return train_delay_status

    def is_afternoon_train_delayed(self):
        train_delay_status = False
        departure_hour = int((self.real_departure_afternoon).split(":")[0])

        official_departure = Basis_Data_From_Schine().get_official_departure('Ingolstadt Nord', 'Regensburg HbF', departure_hour,0,1)
        official_departure_timestamp = datetime.datetime.strptime(official_departure, "%H:%M")
        official_arrival = Basis_Data_From_Schine().get_official_arrival('Ingolstadt Nord', 'Regensburg HbF', departure_hour,0,1)
        official_arrival_timestamp = datetime.datetime.strptime(official_arrival, "%H:%M")

        record_departure_timestamp = datetime.datetime.strptime(self.real_departure_afternoon, "%H:%M")
        record_arrival_timestamp = datetime.datetime.strptime(self.real_arrival_afternoon, "%H:%M")

        if official_departure_timestamp != record_departure_timestamp or official_arrival_timestamp != record_arrival_timestamp:
            train_delay_status = True
        return train_delay_status

def main():
    print(Basis_Data_From_Schine().get_official_departure('Regensburg HbF', 'Ingolstadt Nord', 10, 0, 0))
    print(Basis_Data_From_Schine().get_official_arrival('Regensburg HbF', 'Ingolstadt Nord', 10, 0, 0))
    print(Basis_Data_From_Schine().get_official_departure('Ingolstadt Nord', 'Regensburg HbF', 17, 0, 0))
    print(Basis_Data_From_Schine().get_official_arrival('Ingolstadt Nord', 'Regensburg HbF', 17, 0, 0))

if __name__=="__main__":
    main()
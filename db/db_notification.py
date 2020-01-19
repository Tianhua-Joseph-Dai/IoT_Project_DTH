import schiene
import credentials
import datetime
from pprint import pprint
from prettytable import PrettyTable
import yagmail

class Notification:
    def __init__(self):
            self.gmail_user = 'tiedaibaokou'
            self.email_address = 'tianhua.dai@st.oth-regensburg.de'

    def send_railway_to_email(self, hour, minute):
        subject = 'The railway plan from %s oclock' %hour
        yag = yagmail.SMTP(self.gmail_user, credentials.gmail_app_pwd)
        yag.send(to = self.email_address, subject = subject, contents = Railway_Info().get_railway_plan_Rbg_Ingl(hour, minute))

class Railway_Info:
    def get_railway_plan(self, new_date, new_hour, new_minute, from_station, to_station):
        railway = schiene.Schiene()

        new_time = datetime.time(new_hour, new_minute)
        new_date_time = datetime.datetime.combine(new_date, new_time)

        info_railway_plan=railway.connections(from_station, to_station, dt=new_date_time)
        return info_railway_plan # return type is list

    def get_station_plan(self):
        railway = schiene.Schiene()
        return railway.stations('Ingolstadt Nord')

    def get_railway_plan_Rbg_Ingl(self, hour, minute):
        today_date = datetime.date.today()
        info_table = PrettyTable()
        info_table.field_names = ["From", "To", "Departure", "Arrival", "Duration", "Delay", "Cancel", "Details"]
        for info in self.get_railway_plan(today_date, hour, minute, 'Ingolstadt Nord', 'Regensburg HbF'):
            departure = str(info["departure"])
            arrival = str(info["arrival"])
            transfers = str(info["transfers"])
            duration = str(info["time"])
            ontime_info = info["ontime"]
            products = str(info["products"])
            cancel_status = str(info["canceled"])
            details = "Transfer: {} ({})".format(transfers, products)
            delay = "None"
            if False == ontime_info:
                delay = str(info["delay"])
            info_table.add_row(["Infolstadt Nord", "Regensburg Hbf", departure, arrival, duration, delay, cancel_status, details])
        return info_table.get_string()

def main():
    Notification().send_railway_to_email(15, 0)
    Notification().send_railway_to_email(17, 0)

if __name__=="__main__":
    main()

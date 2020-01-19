import credentials
import os
import db_basic_datas
import time
from datetime import datetime, timedelta
from db_basic_datas import Basis_Data_From_User, Basis_Data_From_Schine
from elasticsearch import Elasticsearch

TOPIC_PREFIX = "dth_IoT_Project_"
now_time = datetime.utcnow()

es = Elasticsearch()
afternoon_departure_hour = int((Basis_Data_From_User().real_departure_afternoon).split(":")[0])

def official_daily_delay_enumerator():
    enumerator = 0
    sub_topic = "official_delay_daily"
    if Basis_Data_From_Schine().is_train_delayed('Regensburg HbF', 'Ingolstadt Nord', 7,0,0):
        enumerator += 1
    elif Basis_Data_From_Schine().is_train_delayed('Ingolstadt Nord', 'Regensburg HbF', afternoon_departure_hour,0,0):
        enumerator += 1
    doc = {}
    doc['time'] = now_time
    doc['topic'] = TOPIC_PREFIX+sub_topic
    doc['frequency'] = enumerator
    res = es.index(index=sub_topic, doc_type='_doc', body=doc)
    print(res['result'])

def real_daily_delay_enumerator():
    enumerator = 0
    sub_topic = "user_delay_daily"
    if Basis_Data_From_User().is_morning_train_delayed():
        enumerator += 1
    elif Basis_Data_From_User().is_afternoon_train_delayed():
        enumerator += 1
    doc = {}
    doc['time'] = now_time
    doc['topic'] = TOPIC_PREFIX + sub_topic
    doc['frequency'] = enumerator
    res = es.index(index=sub_topic, doc_type='_doc', body=doc)
    print(res['result'])

def daily_duration_difference():
    sub_topic = "daily_duration_difference_with_official"
    difference_morning = ((Basis_Data_From_Schine().get_official_duration('Regensburg HbF', 'Ingolstadt Nord', 7,0,0)-Basis_Data_From_User().morning_train_duration)/60)
    difference_afternoon = ((Basis_Data_From_Schine().get_official_duration('Ingolstadt Nord', 'Regensburg HbF', afternoon_departure_hour, 0,
                                                                          0) - Basis_Data_From_User().morning_train_duration)/60)
    doc = {}
    doc['time'] = now_time
    doc['topic'] = TOPIC_PREFIX + sub_topic
    doc['diff_morning'] = difference_morning
    doc['diff_afternoon'] = difference_afternoon
    doc['unit'] = "minutes"
    res = es.index(index=sub_topic, doc_type='_doc', body=doc)
    print(res['result'])

def delayed_train_info_morning():
    number = 0
    sub_topic = "delayed_train"
    delayed_train = Basis_Data_From_Schine().get_train_info('Regensburg HbF', 'Ingolstadt Nord', 7, 0, 0)
    if Basis_Data_From_User().is_morning_train_delayed():
        number += 1
    doc = {}
    doc['time'] = now_time
    doc['topic'] = TOPIC_PREFIX + sub_topic
    doc['number_of_train'] = delayed_train
    doc['delay_frequency'] = number
    res = es.index(index=sub_topic, doc_type='_doc', body=doc)
    print(res['result'])

def delayed_train_info_afternoon():
    number = 0
    sub_topic = "delayed_train"
    delayed_train=Basis_Data_From_Schine().get_train_info('Ingolstadt Nord', 'Regensburg HbF',afternoon_departure_hour,0,0)
    if Basis_Data_From_User().is_afternoon_train_delayed():
        number += 1
    doc = {}
    doc['time'] = now_time
    doc['topic'] = TOPIC_PREFIX + sub_topic
    doc['number_of_train'] = delayed_train
    doc['delay_frequency'] = number
    res = es.index(index=sub_topic, doc_type='_doc', body=doc)
    print(res['result'])

def main():
    official_daily_delay_enumerator()
    real_daily_delay_enumerator()
    time.sleep(2)
    daily_duration_difference()
    time.sleep(2)
    delayed_train_info_morning()
    time.sleep(2)
    delayed_train_info_afternoon()
    time.sleep(2)
    os.remove("/home/dth920312/IoT_Project/record.json")

if __name__=="__main__":
    main()
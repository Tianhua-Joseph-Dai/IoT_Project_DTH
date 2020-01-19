from elasticsearch import Elasticsearch
import paho.mqtt.client as mqtt
import datetime
import pytz
import re
import json
import credentials

es = Elasticsearch()

TOPIC_PREFIX = "/dth/IoT_Project/"
topic_departure = TOPIC_PREFIX+"departure"
topic_arrival = TOPIC_PREFIX+"arrival"

def get_today_date():
    tz = pytz.timezone('Europe/Berlin')
    now = datetime.datetime.now(tz)
    current_date = now.strftime("%m/%-d")
    return current_date

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_departure)
    client.subscribe(topic_arrival)

def on_message(client, userdata, msg):
    # msg.payload is bytes
    str_payload = str(msg.payload)
    sub_topic = msg.topic.split(TOPIC_PREFIX)[1]
    if not 0 == len(re.findall(r'\d\d', str_payload)):
        topic_content=re.findall(r'\d\d', str_payload) # type: list
        # print(topic_content)
    else:
        print("Input error")

    old_data = None
    try:
        with open("/home/dth920312/IoT_Project/record.json", 'r') as load_f:
            old_data=json.load(load_f)
            load_f.close()
    except IOError:
        print("File not accessible")

    if topic_content is not None:
        result = []
        doc = {}
        doc['date'] = get_today_date()
        doc['topic'] = str(msg.topic)
        doc[sub_topic] = "{}:{}".format(topic_content[0], topic_content[1])
        result.append(doc)
        print(result)

        with open("/home/dth920312/IoT_Project/record.json", "w") as dump_f:
            if old_data is not None:
                result.append(old_data)
            print(old_data)
            json.dump(result, dump_f)


client = mqtt.Client()
client.username_pw_set(username=credentials.mqtt_username, password=credentials.mqtt_pwd)
client.on_connect = on_connect
client.on_message = on_message

client.connect(credentials.mqtt_broker, credentials.mqtt_port, 60)
# Blocking call that processes network traffic, dispatches callbacks # and handles reconnecting.
client.loop_forever()
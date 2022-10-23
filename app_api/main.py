import json
import os
from datetime import datetime

import pymongo
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d", rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(os.environ.get("MQTT_TOPIC", "alberto/testing"))


def on_message(client, userdata, msg):
    print("Received message: {} from topic: {}".format(msg.payload.decode(), msg.topic))
    global mongo_db
    try:
        payload = json.loads(msg.payload)
        send_data_mongo(mongo_db, payload)
    except Exception as e:
        print(e)
        print("Error decoding msg, make sure you are sending on a Json valid format")


def send_data_mongo(mongo_db, data):
    try:
        mongo_colection = mongo_db["Testing"]
        data["timestamp"] = datetime.now()
        mongo_colection.insert_one(data)
    except Exception as e:
        print(e)
        print("Error inserting document")


def run():
    client = mqtt.Client()
    client.username_pw_set(username="", password="")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.environ.get("MQTT_BROKER", "test.mosquitto.org"), int(os.environ.get("MQTT_PORT", 1883)))

    client.loop_forever()


if __name__ == '__main__':
    try:
        mongo_client = pymongo.MongoClient(os.environ.get("MONGODB_HOST", ""))
        # conn.server_info()
        mongo_db = mongo_client["IOT_PROJECT"]
    except Exception as e:
        print("Failed to connect to mongo")
    run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import paho.mqtt.client as mqtt_client
import time, random, string, logging, json
from datetime import datetime


# Parameters
use_websockets = False      # Use websockets
use_ssl_tls = False         # Use SSL/TLS
use_credentials = True      # Use credentials to connect to the host
use_debug_log = False       # Activate debug log
subscribe_topic = False     # Activate topic subscription
publish_message = True      # Activate message publication
publish_interval = 1        # Publish message interval (in seconds)


# Create random string to use in ClientID
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


# Configurations
mqtt_host = "xxxxxxxxxx"
if use_websockets:
    mqtt_port = 8081
else:
    mqtt_port = 8883
mqtt_keepalive_interval = 60
mqtt_topic = "xxxxxxxxxx"
if use_credentials:
    mqtt_username = "xxxxxxxxxx"
    mqtt_password = "xxxxxxxxxx"
mqtt_clientid = "python-mqtt-{}".format(get_random_alphanumeric_string(15))
if use_ssl_tls:
    mqtt_tls = "xxxxxxxxxx"
mqtt_qos  = 0
mqtt_retain = False
connected = False
print("\nHost:\t\t{}\nPort:\t\t{}\nTopic:\t\t{}\nUsername:\t{}\nPassword:\t{}\nClientID:\t{}\n".format(mqtt_host, mqtt_port, mqtt_topic, mqtt_username, mqtt_password, mqtt_clientid))


# Create message to publish
def create_message():
    t = round(random.uniform(0, 1)*100,2)
    hr = round(random.uniform(0, 1)*100,2)
    ts = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data = {}
    data['Timestamp'] = ts
    data['Temperatura'] = t
    data['Humidade'] = hr
    json_data = json.dumps(data)
    return json_data


# Connect to MQTT Broker
def connect_mqtt():

    # Create MWTT Client
    if use_websockets:
        client = mqtt_client.Client(client_id=mqtt_clientid, clean_session=True, transport="websockets")
        if use_ssl_tls:
            client.tls_set(mqtt_tls) # Use only for SSL/TLS certificate
        else:
            client.tls_set()
    else:
        client = mqtt_client.Client(client_id=mqtt_clientid, clean_session=True)

    # Set Client username and password
    if use_credentials:
        client.username_pw_set(mqtt_username, mqtt_password)

    # onConnect Function
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker with success!\n")
            global connected
            connected = True
        else:
            print("Failed to connect with return code '{}'".format(rc))    
    client.on_connect = on_connect

    # onLog Function
    if use_debug_log:
        def on_log(mqttc, obj, level, string):
            print(string)
        client.on_log = on_log

    # Connect to Client
    client.connect(mqtt_host, mqtt_port, mqtt_keepalive_interval)

    return client


# Publish Function
def publish(client):
    
    # onPublish Function
    def on_publish(client, userdata, mid):
        print("Message published on topic '{}': {}".format(mqtt_topic, msg))
    client.on_publish = on_publish

    # Start loop
    client.loop_start()

    # Wait Client Connection
    while connected != True:
        time.sleep(0.1)

    # Publish
    try:
        while True:
            msg = create_message()
            client.publish(mqtt_topic, msg, mqtt_qos, mqtt_retain)
            time.sleep(publish_interval)

    # Disconnect Client and stop loop
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()


# Subscribe Function
def subscribe(client):

    # onSubscribe Function
    def on_subscribe(client, obj, mid, granted_qos):
        print("Topic '{}' subscribed with success!\n".format(mqtt_topic))
    client.on_subscribe = on_subscribe

    # onMessage Function
    def on_message(client, userdata, message):
        print("Message received:", str(message.payload.decode("utf-8")))
    client.on_message = on_message


    # Subscribe
    try:
        client.subscribe(mqtt_topic, mqtt_qos)
        # Start loop
        client.loop_forever()

    # Disconnect Client and stop loop
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()


# Main function
def run_mqtt_publisher():
    client = connect_mqtt()
    if not publish_message and not subscribe_topic:
        print("Please enable publish or subscribe!\n")
    if publish_message and subscribe_topic:
        print("Please enable only one of the publish or subscribe options!\n")
        return
    if publish_message:
        publish(client)
    if subscribe_topic:
        subscribe(client)


if __name__ == '__main__':
    run_mqtt_publisher()

    # Sources: https://www.emqx.io/blog/how-to-use-mqtt-in-python
    #          https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_sub.py
    #          https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_logger.py
    #          https://stackoverflow.com/a/41790701/7066664

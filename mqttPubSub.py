#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import paho.mqtt.client as mqtt_client
import time, random, string, logging, json
from datetime import datetime


# Configurations
use_websockets = False      # Use websockets
use_ssl_tls = False         # Use SSL/TLS
use_credentials = False      # Use credentials to connect to the host
use_debug_log = False       # Activate debug log
subscribe_topic = False     # Activate topic subscription
publish_message = True      # Activate message publication
publish_interval = 1        # Publish message interval (in seconds)


# Parameters
mqtt_host = "test.mosquitto.org"
mqtt_port = 1883
mqtt_username = ""
mqtt_password = ""
mqtt_ssl_tls = ""
mqtt_topic = "test_topic_mqtt"
mqtt_qos  = 0
mqtt_retain = False
mqtt_keepalive_interval = 60


# Show parameters
mqtt_clientid = "python-mqtt-{}".format(''.join(random.choice(string.ascii_letters + string.digits) for i in range(15)))
connected = False
print("\nHost:\t\t\t{}\nPort:\t\t\t{}\nUsername:\t\t{}\nPassword:\t\t{}\nSSL/TLS certificate:\t{}\nTopic:\t\t\t{}\nClientID:\t\t{}\nQoS:\t\t\t{}\nRetain:\t\t\t{}\n".format(mqtt_host, mqtt_port, mqtt_username if use_credentials else 'use_credentials not activated', mqtt_password if use_credentials else 'use_credentials not activated', mqtt_ssl_tls if use_ssl_tls else 'use_ssl_tls not activated', mqtt_topic, mqtt_clientid, mqtt_qos, mqtt_retain))


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
            client.tls_set(mqtt_ssl_tls) # Use only for SSL/TLS certificate
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

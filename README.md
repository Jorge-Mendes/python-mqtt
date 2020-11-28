# MQTT Python Client

This repository provides a python script that allows you to both publish and subscribe messages via [MQTT](https://mqtt.org/) using [paho-mqtt](https://pypi.org/project/paho-mqtt/) library.

## Table of Contents
1. [How to install](#howtoinstall)
2. [How to configure](#howtoconfigure)
2. [How to run](#howtorun)
3. [Screenshots](#screenshots)

## How to install <a name="howtoinstall"></a>

```
pip install -r requirements.txt
```

## How to configure <a name="howtoconfigure"></a>

The script configurations can be made in the [Configurations](https://github.com/Jorge-Mendes/python-mqtt/blob/main/mqttPubSub.py#L10-L17) and [Parameters](https://github.com/Jorge-Mendes/python-mqtt/blob/main/mqttPubSub.py#L20-L29) sections of the script.

| Configurations   |                                        |               |
|------------------|----------------------------------------|---------------|
| use_websockets   | Use websockets                         | True/False    |
| use_ssl_tls      | Use SSL/TLS                            | True/False    |
| use_credentials  | Use credentials to connect to the host | True/False    |
| use_debug_log    | Activate debug log                     | True/False    |
| subscribe_topic  | Activate topic subscription            | True/False    |
| publish_message  | Activate message publication           | True/False    |
| publish_interval | Publish message interval (in seconds)  | Integer value |

<br>

| Parameters              |           |  Cool |
|-------------------------|-------------|------:|
| mqtt_host               | MQTT broker host     | $1600 |
| mqtt_port               | MQTT broker port     | $1600 |
| mqtt_username           | MQTT broker username | $1600 |
| mqtt_password           | MQTT broker password | $1600 |
| mqtt_ssl_tls            |  left-aligned | $1600 |
| mqtt_topic              |  left-aligned | $1600 |
| mqtt_qos                |  left-aligned | $1600 |
| mqtt_retain             |  left-aligned | $1600 |
| mqtt_keepalive_interval |  left-aligned | $1600 |




## How to run <a name="howtorun"></a>

```
python mqttPubSub.py
```

## Screenshots <a name="screenshots"></a>

...
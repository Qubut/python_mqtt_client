from paho.mqtt.client import Client as mqtt_client
import logging
from os import environ


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.error(f"Failed to connect, return code {rc}")

    client = mqtt_client(environ.get('MQTT_CLIENT_ID'))

    if (user := environ.get('MQTT_USER')) and (passwd := environ.get('MQTT_PASSWD')):
        client.username_pw_set(user, passwd)
    else:
        logging.warning(
            """No credentials were provided
            Trying to connect as anonymous""")
    client.on_connect = on_connect
    if (broker := environ.get('MQTT_BROKER')) and (port := environ.get('MQTT_PORT')):
        client.connect(broker, port)
    else:
        logging.warning("""Broker's IP and Port weren't provided
                        Using default: localhost:1883""")
        client.connect("localhost", 1883)
    return client

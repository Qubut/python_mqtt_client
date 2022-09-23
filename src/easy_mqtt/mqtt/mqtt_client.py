from paho.mqtt.client import Client
from os import environ
from utils import logger


class MqttClient:

    def __init__(self, topic: str, qos: int = 0, client_id: str | None = None,):
        self.topic = topic
        self.qos = qos
        if client_id := environ.get('MQTT_CLIENT_ID'):
            self.client = Client(client_id)

        self.client = Client()
        if (user := environ.get('MQTT_USER')) and (passwd := environ.get('MQTT_PASSWD')):

            self.client.username_pw_set(user, passwd)
        else:
            logger.warning(
                """No credentials were provided""")
        if (broker := environ.get('MQTT_BROKER')) and (port := environ.get('MQTT_PORT')):
            self.client.connect(broker, int(port))
        else:
            logger.warning("""Broker's IP and Port weren't provided
                        Using default: localhost:1883""")
            self.client.connect('localhost',1883)
            self.client.on_connect = lambda client, userdata, flags, rc: logger.info(
                "Connected to MQTT Broker!") if rc == 0 else logger.error(f"Failed to connect, return code {rc}")

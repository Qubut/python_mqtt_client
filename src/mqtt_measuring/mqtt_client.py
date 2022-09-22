from paho.mqtt.client import Client
from os import environ
from .logger import logger


class MqttClient:

    def __init__(self, client_id: str | None = None):
        if client_id := environ.get('MQTT_CLIENT_ID'):
            self.client = Client(client_id)

        self.client = Client()
        if (user := environ.get('MQTT_USER')) and (passwd := environ.get('MQTT_PASSWD')):

            self.client.username_pw_set(user, passwd)
        else:
            logger.warning(
                """No credentials were provided""")

    def connect(self):
        if (broker := environ.get('MQTT_BROKER')) and (port := environ.get('MQTT_PORT')):
            self.client.connect(broker, int(port))
        else:
            logger.warning("""Broker's IP and Port weren't provided
                        Using default: localhost:1883""")
            self.client.on_connect = self.on_connect
            self.client.connect_async("localhost", 1883)

    def on_connect(self, client: Client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
            print(client.is_connected())
        else:
            logger.error(f"Failed to connect, return code {rc}")

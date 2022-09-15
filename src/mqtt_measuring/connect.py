from paho.mqtt.client import Client as mqtt_client

broker = '192.168.0.16'
port = 1883
client_id = ""


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

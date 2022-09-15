from paho.mqtt.client import Client as mqtt_client
from timing import timed
from connect import connect_mqtt
from argparse import ArgumentParser
import time



filename = "DUMMYFILE"

def onMessage(client:mqtt_client, userdata,message):
    print("Recieving Message")
    print(message.topic)
    print(message.payload)
    savePayload(client,message.payload,filename)

@timed
def savePayload(client:mqtt_client,payload, filename):
    print(f"Saving {filename}")
    with open(filename,"wb") as f:
        f.write(payload)

def subscribe(client:mqtt_client,topic):
    client.subscribe(topic)
    client.on_message = onMessage

def run(topic:str):
    client = connect_mqtt()
    # while client.is_connected == True:
    #     time.sleep(1)
    subscribe(client,topic)
    client.loop_forever()
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("topic")
    topic = parser.parse_args()._get_kwargs()[0][1]
    run(topic)

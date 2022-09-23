from mqtt_client import MqttClient
import subscribe
import publish
import click

def main():
    el = MqttClient()
    el.connect()
    subscribe(el.client, topic)
    el.client.loop_forever()

if __name__=="__main__":
    main()
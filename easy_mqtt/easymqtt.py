from commands import publish, subscribe
import click


@click.group(help="""Cli tool for sending data or messages between MQTT clients""")
def easy_mqtt():
    ...


easy_mqtt.add_command(publish.publish)
easy_mqtt.add_command(subscribe.subscribe)

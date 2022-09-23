import click
from mqtt.mqtt_subscribe import MqttSubscribe
from utils import logger
from utils import check_path, mk_dir


def run(topic: str, qos: int, output_dir: str):
    el = MqttSubscribe(topic, qos, output_dir)
    client = el.client
    client.subscribe(topic)
    client.loop_forever()


@click.command()
@click.option("--topic", "-t", default="/home/file", type=str, help="sets the message's topic")
@click.option("--qos", "-q", default='0', type=click.Choice(['0', '1', '2']), help="defines the QoS")
@click.option("--output-dir", "-od", type=click.Path(exists=1,
                                                     file_okay=0,
                                                     writable=1,
                                                     executable=1),
              help="Directory of transmitted files")
def subscribe(topic, qos, output_dir):
    if not check_path(output_dir):
        try:
            mk_dir(output_dir)
        except Exception as e:
            logger.error(e)
            return 1
    run(topic, int(qos), output_dir)


if __name__ == '__main__':
    subscribe()

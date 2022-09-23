import click
from mqtt_subscribe import MqttSubscribe
from utils import logger
from utils import check_path, mk_dir


def run(topic: str, qos: int, od: str):
    el = MqttSubscribe(topic, qos, od)
    client = el.client
    client.subscribe(topic)
    client.loop_forever()


@click.command()
@click.option("--topic", "-t", default="/home/file", type=str, help="sets the message's topic")
@click.option("--qos", "-q", default='0', type=click.Choice(['0', '1', '2']), help="defines the QoS")
@click.option("--output-dir", "-od", type=str, help="Directory of transmitted files")
def subscribe(topic, qos, output_dir):
    od = output_dir
    if not check_path(od):
        try:
            mk_dir(od)
        except Exception as e:
            logger.error(e)
            return 1
    run(topic, int(qos), od)


if __name__ == '__main__':
    subscribe()

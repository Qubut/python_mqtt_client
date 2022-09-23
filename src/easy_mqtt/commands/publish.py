from mqtt.mqtt_publish import MqttPublish
from utils import logger, check_file
import click


def run(topic: str, message: str, qos: int,  retain: bool, file: str, chunk_size):
    el = MqttPublish(topic, qos)
    el.chunk_size = chunk_size
    client = el.client
    if file:
        el.send_file(client, topic,  qos, retain, file)
        # publish_thread = threading.Thread(
        #     target=el.send_file, args=(client, topic, file, qos, retain))
        # publish_thread.daemon = True
        # publish_thread.start()
        # publish_thread.join()
    if message:
        client.publish(topic, message, qos,  retain)
    client.loop_forever()


@click.command()
@click.option("--qos", "-q", default=0, type=click.Choice([0, 1, 2]), help="defines the QoS")
@click.option("--topic", "-t", default="/home/file", type=str, help="sets the message's topic")
@click.option("--message", "-m", default=None, type=str, help="message to be sent to the subscribers")
@click.option("--file", "-f", type=click.Path(exists=1, dir_okay=0), help="file to be sent to the subscribers")
@click.option("--retain", "-r", default=False, type=bool, help="""if set to True, 
              the will message will be set as the “last known good”/retained message for the topic""")
@click.option("--chunk-size", "-cs", default="1024", type=str, help="""sets the chunk size of the file 
                                                                    per payload""")
def publish(topic, message, file, qos, retain, chunk_size):
    if not file and not message:
        raise click.MissingParameter('No message or file were provided')
    elif file:
        logger.info(
            f"starting the transfer of file {file}  chunksize = {chunk_size} byte")
    run(topic, message, qos, retain,  file, chunk_size)

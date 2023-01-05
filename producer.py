import pika
import json

from constans import USERNAME_AMQP, PASSWORD_AMQP

cloud_url_rabbitmq = f"amqps://{USERNAME_AMQP}:{PASSWORD_AMQP}@kebnekaise.lmq.cloudamqp.com/qcwoiucd"
params = pika.URLParameters(cloud_url_rabbitmq)
conection = pika.BlockingConnection(params)

channel = conection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="api_users_comics",
        body=json.dumps(body).encode(),
        properties=properties
    )

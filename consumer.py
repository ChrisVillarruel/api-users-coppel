import pika

from constans import USERNAME_AMQP, PASSWORD_AMQP

cloud_url_rabbitmq = f"amqps://{USERNAME_AMQP}:{PASSWORD_AMQP}@kebnekaise.lmq.cloudamqp.com/qcwoiucd"
params = pika.URLParameters(cloud_url_rabbitmq)
conection = pika.BlockingConnection(params)

channel = conection.channel()
channel.queue_declare(queue="api_users")


def callback(ch, method, properties, body):
    print("Received in ApiUser")
    print(body)


channel.basic_consume(queue="api_users", on_message_callback=callback)
print("Started consuming")
channel.start_consuming()
channel.close()

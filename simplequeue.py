import socket
import time
import os
import pika

# receiving message callback
def receiveMessage(channel, method, properties, body):
    print('[x] Received %r ' % body)


print('**** Running simplequeue.py ****')

amqp_url = os.environ['AMQP_URL']
print(amqp_url)

urlConnectionParameters = pika.URLParameters(amqp_url)

# # ### choose which parameter set
parameters = urlConnectionParameters
   
try:
    print('[x] about to build a blocking connection')
    connection = pika.BlockingConnection(parameters)
    print('[x] built a connection')
    channel = connection.channel()
    channel.queue_declare(queue='first_queue')

    channel.basic_publish(exchange='', routing_key='first_queue', body='Hi Queue')
    print('[x] send a first message to the queue')


    time.sleep(5)

    channel.basic_consume(queue='first_queue', auto_ack=True, on_message_callback=receiveMessage)

    print('[x] Waiting for messages')

    channel.start_consuming()
    connection.close()
except:
    print("[!] We could not get a connection")
    pass
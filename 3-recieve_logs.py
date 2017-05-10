#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

#once we disconnect the consumer the queue should be deleted
result = channel.queue_declare(exclusive=True)                         
queue_name = result.method.queue # gives an random named queue

#bind the queue to the logs exchange
#rabbitmqctl list_bindings to list bindings
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print (" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack = True)

channel.start_consuming()




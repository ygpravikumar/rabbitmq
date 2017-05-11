#!usr/bin/env python

import pika
import sys

# create a blocking connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

#declare the direct_logs exchange
channel.exchange_declare(exchange='direct_logs', 
                         type='direct')

#get a new random named queue from the exchange
result=channel.queue_declare(exclusive=True)#make the queue auto deleted when connection gets closed
queue_name = result.method.queue

#get the severities to listen to from the user
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

#bind the severities to the queue
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

#define the calback
def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

#register the callback for the queue
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

#start consuming
channel.start_consuming()

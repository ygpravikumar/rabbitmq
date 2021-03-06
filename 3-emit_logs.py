#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#declare a named exchange of type fanout
channel.exchange_declare(exchange='logs', type='fanout')

message = ''.join(sys.argv[1:]) or "info : Hello World!"

#send message to our logs exchange
channel.basic_publish(exchange='logs',
                        routing_key='',
                        body=message)

print(' [x] Sent %r' % message)

connection.close()


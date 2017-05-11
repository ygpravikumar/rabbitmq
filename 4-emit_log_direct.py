#!usr/bin/env python

import pika
import sys

# Create a blocking connection to rabbitmq server running on local host
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# get a channel
channel = connection.channel()

# declare the direct_logs exchange if it doesnot already exists and set its type to direct
channel.exchange_declare(exchange='direct_logs',
                         type='direct')

# get the severity from console
severity = sys.argv[1] if len(sys.argv) > 2 else 'info'

# get the message from console
message = ''.join(sys.argv[2:]) or "Hello World!"

# publish the message to direct_logs exchange along with its severity
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)

# close the connection
connection.close()

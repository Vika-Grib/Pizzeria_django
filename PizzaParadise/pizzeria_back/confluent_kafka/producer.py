from confluent_kafka import Producer
import socket
import consumer

conf = {'bootstrap.servers': 'localhost',
        'client.id': socket.gethostname()}

producer = Producer(conf)
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

producer.produce('topic', key="key", value="value", callback=acked)

# Wait up to 1 second for events. Callbacks will be invoked during
# this method call if the message is acknowledged.
producer.poll(1)
consumer.consume_loop(topics=['topic'])

#producer.flush(30)
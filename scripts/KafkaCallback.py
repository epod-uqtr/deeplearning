import logging
import sys
import time
from datetime import datetime

import tensorflow as tf
from confluent_kafka import Producer
from confluent_kafka import Consumer


class KafkaCallback(tf.keras.callbacks.Callback):

    train_id = 0
    test_id = 0
    predict_id = 0
    bootstrap_servers = "127.0.0.1:9091"
    consumer_group_id = "foo"
    topic = 'deeplearning_training'
    username = 'zinnour'
    producer_conf = {'bootstrap.servers': bootstrap_servers}
    producer = Producer(producer_conf)
    time = int(round(time.time() * 1000))
    consumer_conf = {'bootstrap.servers': bootstrap_servers,
                     'group.id': consumer_group_id,
                     'auto.offset.reset': 'earliest'}
    consumer = Consumer(consumer_conf)

    def __init__(self, training_time):
        super().__init__()
        self.training_time = training_time

    def on_train_begin(self, logs=None):
        self.consumer.subscribe([self.topic])

    def consume_messages(self):
        msg = self.consumer.poll()

        if msg.error():
            print("Consumer error: {}".format(msg.error()))
        else:
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                             (msg.topic(), msg.partition(), msg.offset(),
                              str(msg.key())))
            print(msg.value())

    def on_train_batch_end(self, batch, logs=None):
        self.train_id += 1
        value = {
            'id': self.train_id,
            'type': 'train',
            'batch': batch,
            'loss': logs['loss'],
            'accuracy': logs['accuracy']
        }
        self.producer.poll(0)
        self.producer.produce(self.topic, key=self.username + "_" + str(self.training_time), value=str(value),
                              callback=self.delivery_report)
        self.consume_messages()
        # self.producer.flush()

    def on_test_batch_end(self, batch, logs=None):
        self.test_id += 1
        value = {
            'id': self.test_id,
            'type': 'test',
            'batch': batch,
            'loss': logs['loss'],
            'accuracy': logs['accuracy']
        }
        self.producer.poll(0)
        self.producer.produce(self.topic, key=self.username + "_" + str(self.training_time), value=str(value),
                              callback=self.delivery_report)
        self.consume_messages()

    def on_predict_batch_end(self, batch, logs=None):
        self.predict_id += 1
        value = {
            'id': self.predict_id,
            'type': 'predict',
            'batch': batch,
            'loss': logs['loss'],
            'accuracy': logs['accuracy']
        }
        self.producer.poll(0)
        self.producer.produce(self.topic, key=self.username + "_" + str(self.training_time), value=str(value),
                              callback=self.delivery_report)
        self.consume_messages()

    @staticmethod
    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def on_predict_end(self, logs=None):
        self.consumer.close()



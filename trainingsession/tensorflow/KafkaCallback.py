import logging
import sys
import time
from datetime import datetime

import tensorflow as tf
from confluent_kafka import Producer
from confluent_kafka import Consumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class KafkaCallback(tf.keras.callbacks.Callback):
    train_id = 0
    test_id = 0
    predict_id = 0
    bootstrap_servers = "127.0.0.1:9091"
    consumer_group_id = "foo"
    topic = 'deeplearning_training'
    username = 'lacen'
    producer_conf = {'bootstrap.servers': bootstrap_servers}
    producer = Producer(producer_conf)
    time = int(round(time.time() * 1000))
    consumer_conf = {'bootstrap.servers': bootstrap_servers,
                     'group.id': consumer_group_id,
                     'auto.offset.reset': 'earliest'}
    consumer = Consumer(consumer_conf)
    channel_layer = get_channel_layer()

    def on_train_begin(self, logs=None):
        self.consumer.subscribe([self.topic])

    def consume_kafka_messages(self):
        print('---------------')
        msg = self.consumer.poll()

        if msg.error():
            print("Consumer error: {}".format(msg.error()))
        else:
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                             (msg.topic(), msg.partition(), msg.offset(),
                              str(msg.key())))
            print(msg.value())
            value = json.loads(msg.value())
            print(value['batch'])

            async_to_sync(self.channel_layer.group_send)(
                "zinnour",
                {'type': 'train.consume_msg',
                 'key': msg.key(),
                 'id': value['id'],
                 'method': value['method'],
                 'batch': value['batch'],
                 'loss': value['loss'],
                 'accuracy': value['accuracy']}
            )

    def on_train_batch_end(self, batch, logs=None):
        self.train_id += 1
        value = {
            'id': self.train_id,
            'method': 'train',
            'batch': batch,
            'loss': logs['loss'],
            'accuracy': logs['accuracy']
        }
        self.producer.poll(0)
        self.producer.produce(self.topic, key=self.username + "_" + str(self.time), value=str(value),
                              callback=self.delivery_report)


        # self.producer.flush()

    def on_test_batch_end(self, batch, logs=None):
        self.test_id += 1
        value = {
            'id': self.test_id,
            'method': 'test',
            'batch': batch,
            'loss': logs['loss'],
            'accuracy': logs['accuracy']
        }
        self.producer.poll(0)
        self.producer.produce(self.topic, key=self.username + "_" + str(self.time), value=str(value),
                              callback=self.delivery_report)

    def on_predict_batch_end(self, batch, logs=None):
        self.predict_id += 1
        value = {
            'id': self.predict_id,
            'method': 'predict',
            'batch': batch,
            'loss': logs['loss'],
            'accuracy': logs['accuracy']
        }
        self.producer.poll(0)
        self.producer.produce(self.topic, key=self.username + "_" + str(self.time), value=str(value),
                              callback=self.delivery_report)

    @staticmethod
    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
            self.consume_kafka_messages()


    def on_predict_end(self, logs=None):
        self.consumer.close()

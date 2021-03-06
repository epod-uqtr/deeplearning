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
    consumer_group_id = "deeplearning"
    topic = "deeplearning-training"
    username = "lacen"
    producer_conf = {"bootstrap.servers": bootstrap_servers}
    producer = Producer(producer_conf)
    time = int(round(time.time() * 1000))
    consumer_conf = {"bootstrap.servers": bootstrap_servers,
                     "group.id": consumer_group_id,
                     "auto.offset.reset": "earliest"}
    consumer = Consumer(consumer_conf)
    i_train = 0
    epoch = -1
    channel_layer = get_channel_layer()

    def __init__(self, session_name):
        super().__init__()
        self.session_name = session_name
        print("---------------  session_name= "+ session_name)

    def on_train_begin(self, logs=None):
        self.consumer.subscribe([self.topic])

    @classmethod
    def consume_kafka_messages(self, cls):
        print("---------------")
        msg = cls.consumer.poll()

        if msg.error():
            print("Consumer error: {}".format(msg.error()))
        else:
            sys.stderr.write("%% %s [%d] at offset %d with key %s:\n" %
                             (msg.topic(), msg.partition(), msg.offset(),
                              str(msg.key())))
            print(msg.value().decode("utf-8"))
            value = json.loads(msg.value().decode("utf-8"))
            print(value["batch"])

            async_to_sync(cls.channel_layer.group_send)(
                self.session_name,
                {"type": "train.consume_msg",
                 "key": msg.key(),
                 "id": value["id"],
                 "method": value["method"],
                 "batch": value["batch"],
                 "loss": value["loss"],
                 "accuracy": value["accuracy"]}
            )

    def on_epoch_begin(self, epoch, logs=None):
        self.epoch = epoch

    def on_train_batch_end(self, batch, logs=None):
        #print(logs)
        self.train_id += 1
        value = {
            "id": self.train_id,
            "method": "train",
            "epoch": self.epoch,
            "batch": batch,
            "loss": logs["loss"],
            "accuracy": logs["accuracy"]
        }
        self.producer.poll(0)
        self.producer.produce(self.topic, key=self.username + "_" + str(self.time), value=str(value),
                              callback=self.delivery_report)
        # if batch % 10 == 0:
        async_to_sync(self.channel_layer.group_send)(self.session_name,
            {'type': "training_session_message",
             'data': json.dumps(value)})
        self.i_train = self.i_train + 1
        # self.producer.flush()

    # def on_test_batch_end(self, batch, logs=None):
    #     self.test_id += 1
    #     value = {
    #         "id": self.test_id,
    #         "method": "test",
    #         "batch": batch,
    #         "loss": logs["loss"],
    #         "accuracy": logs["accuracy"]
    #     }
    #     self.producer.poll(0)
    #     self.producer.produce(self.topic, key=self.username + "_" + str(self.time), value=str(value),
    #                           callback=self.delivery_report)
    #
    #     async_to_sync(self.channel_layer.group_send)(self.session_name,
    #         {"type": "training_session_message",
    #          'data': json.dumps(value)})


    @staticmethod
    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))
            # KafkaCallback.consume_kafka_messages()




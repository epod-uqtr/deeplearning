# TensorFlow and tf.keras
import sys

import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np

from scripts.KafkaCallback import KafkaCallback
#import tensorflow_io as tfio
import keras_metrics as km


def main(session_name, epochs, batch_size, optimizer, loss, metrics):
    # kafka_dataset = tfio.kafka.KafkaDataset(
    #     topics='deeplearnint_training_1', servers='localhost', group='', eof=False, timeout=1000,
    #     config_global=None, config_topic=None, message_key=False
    # )

    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])
    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=metrics)
    model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, callbacks=[KafkaCallback(session_name)])
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2, callbacks=[KafkaCallback(session_name)])

    print('\nTest accuracy:', test_acc)


if __name__ == "__main__":
    METRICS = [
        keras.metrics.SparseCategoricalAccuracy(),
        km.precision(),
    ]

    main(session_name=sys.argv[1],
         epochs=int(sys.argv[2]),
         batch_size=int(sys.argv[3]),
         optimizer=sys.argv[4],
         loss=sys.argv[5],
         metrics=METRICS)

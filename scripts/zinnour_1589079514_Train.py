# TensorFlow and tf.keras
import sys

import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np

from scripts.KafkaCallback import KafkaCallback


def main(session_name, epochs, batch_size, optimizer, loss, metrics):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])
    model.compile(optimizer=optimizer,
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=metrics)
    model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, callbacks=[KafkaCallback(session_name)])
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2, callbacks=[KafkaCallback(session_name)])

    print('\nTest accuracy:', test_acc)


if __name__ == "__main__":
    main(session_name=sys.argv[1],
         epochs=sys.argv[2],
         batch_size=sys.argv[3],
         optimizer=sys.argv[4],
         loss=sys.argv[5],
         metrics=sys.argv[6])

# TensorFlow and tf.keras
import sys

import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np

from scripts.KafkaCallback import KafkaCallback


def main(time):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=10, batch_size=64, callbacks=[KafkaCallback()])
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2, callbacks=[KafkaCallback()])

    print('\nTest accuracy:', test_acc)


if __name__ == "__main__":
    main(sys.argv[1])

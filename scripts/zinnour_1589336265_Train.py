# TensorFlow and keras
import sys

import tensorflow as tf

# Helper libraries
import numpy as np

from scripts.KafkaCallback import KafkaCallback
# import tensorflow_io as tfio
import keras_metrics as km
import keras

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
        'accuracy',keras.metrics.TrueNegatives()
    ]
    LOSS = [
        (1, keras.losses.BinaryCrossentropy(from_logits=True), 'Binary crossentropy'),
        (2, keras.losses.CategoricalCrossentropy(from_logits=True), 'Categorical crossentropy'),
        (3, keras.losses.CategoricalHinge(), 'Categorical hinge'),
        (5, keras.losses.Hinge(), 'Hinge'),
        (5, keras.losses.Hinge(), 'Hinge'),
        (6, keras.losses.Huber(), 'Huber'),
        (7, keras.losses.SquaredHinge(), 'Squared hinge'),
        (8, keras.losses.LogCosh(), 'Hyperbolic Cosine'),
        (9, keras.losses.MeanAbsoluteError(), 'Mean absolute error'),
        (10, keras.losses.MeanAbsolutePercentageError(), 'Mean absolute percentage error'),
        (11, keras.losses.MeanSquaredError(), 'Mean squared error'),
        (12, keras.losses.MeanSquaredLogarithmicError(), 'Mean squared logarithmic error (MSLE)'),
        (13, keras.losses.Poisson(), 'Poisson'),
        (14, keras.losses.SparseCategoricalCrossentropy(from_logits=True), 'Sparse categorical crossentropy'),
    ]
    main(session_name=sys.argv[1],
         epochs=int(sys.argv[2]),
         batch_size=int(sys.argv[3]),
         optimizer=sys.argv[4],
         loss=LOSS[int(sys.argv[5]) - 1][1],
         metrics=METRICS)

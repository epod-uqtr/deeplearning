# TensorFlow and tf.keras
import sys

import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from tensorflow import keras

# Helper libraries
import numpy as np

from scripts.CategoricalFalsePositives import CategoricalFalsePositives
from scripts.CategoricalTrueNegatives import CategoricalTrueNegatives
from scripts.CategoricalTruePositives import CategoricalTruePositives
from scripts.KafkaCallback import KafkaCallback
#import tensorflow_io as tfio
import keras_metrics as km
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
import os
import numpy as np


def main(session_name, epochs, batch_size, optimizer, loss, metrics):
    # kafka_dataset = tfio.kafka.KafkaDataset(
    #     topics='deeplearnint_training_1', servers='localhost', group='', eof=False, timeout=1000,
    #     config_global=None, config_topic=None, message_key=False
    # )

    _URL = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'

    path_to_zip = tf.keras.utils.get_file('cats_and_dogs.zip', origin=_URL, extract=True)

    PATH = os.path.join(os.path.dirname(path_to_zip), 'cats_and_dogs_filtered')
    train_dir = os.path.join(PATH, 'train')
    validation_dir = os.path.join(PATH, 'validation')
    train_cats_dir = os.path.join(train_dir, 'cats')  # directory with our training cat pictures
    train_dogs_dir = os.path.join(train_dir, 'dogs')  # directory with our training dog pictures
    validation_cats_dir = os.path.join(validation_dir, 'cats')  # directory with our validation cat pictures
    validation_dogs_dir = os.path.join(validation_dir, 'dogs')  # directory with our validation dog pictures
    num_cats_tr = len(os.listdir(train_cats_dir))
    num_dogs_tr = len(os.listdir(train_dogs_dir))

    num_cats_val = len(os.listdir(validation_cats_dir))
    num_dogs_val = len(os.listdir(validation_dogs_dir))

    total_train = num_cats_tr + num_dogs_tr
    total_val = num_cats_val + num_dogs_val

    print('total training cat images:', num_cats_tr)
    print('total training dog images:', num_dogs_tr)

    print('total validation cat images:', num_cats_val)
    print('total validation dog images:', num_dogs_val)
    print("--")
    print("Total training images:", total_train)
    print("Total validation images:", total_val)

    batch_size = 128
    epochs = 15
    IMG_HEIGHT = 150
    IMG_WIDTH = 150
    train_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our training data
    validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our validation data
    train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                               directory=train_dir,
                                                               shuffle=True,
                                                               target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                               class_mode='binary')
    val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                                  directory=validation_dir,
                                                                  target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                                  class_mode='binary')
    sample_training_images, _ = next(train_data_gen)

    model = Sequential([
        Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        MaxPooling2D(),
        Conv2D(32, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Conv2D(64, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(1)
    ])
    # model.compile(optimizer=optimizer,
    #               loss=loss,
    #               metrics=metrics)
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    model.summary()

    # model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, callbacks=[KafkaCallback(session_name)])
    # test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2, callbacks=[KafkaCallback(session_name)])

    history = model.fit(
        train_data_gen,
        steps_per_epoch=total_train // batch_size,
        epochs=epochs,
        validation_data=val_data_gen,
        validation_steps=total_val // batch_size,
        callbacks=[KafkaCallback(session_name)]
    )

    #print('\nTest accuracy:', test_acc)


if __name__ == "__main__":
    METRICS = [
        'accuracy',
        CategoricalTruePositives(10, 64),
        CategoricalTrueNegatives(10, 64),
        CategoricalFalsePositives(10, 64)
    ]
    LOSS = [
        (1, tf.keras.losses.BinaryCrossentropy(from_logits=True), 'Binary crossentropy'),
        (2, tf.keras.losses.CategoricalCrossentropy(from_logits=True), 'Categorical crossentropy'),
        (3, tf.keras.losses.CategoricalHinge(), 'Categorical hinge'),
        (4, tf.keras.losses.CosineSimilarity(), 'Cosine similarity'),
        (5, tf.keras.losses.Hinge(), 'Hinge'),
        (6, tf.keras.losses.Huber(), 'Huber'),
        (7, tf.keras.losses.SquaredHinge(), 'Squared hinge'),
        (8, tf.keras.losses.LogCosh(), 'Hyperbolic Cosine'),
        (9, tf.keras.losses.MeanAbsoluteError(), 'Mean absolute error'),
        (10, tf.keras.losses.MeanAbsolutePercentageError(), 'Mean absolute percentage error'),
        (11, tf.keras.losses.MeanSquaredError(), 'Mean squared error'),
        (12, tf.keras.losses.MeanSquaredLogarithmicError(), 'Mean squared logarithmic error (MSLE)'),
        (13, tf.keras.losses.Poisson(), 'Poisson'),
        (14, tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 'Sparse categorical crossentropy'),
    ]
    main(session_name=sys.argv[1],
         epochs=int(sys.argv[2]),
         batch_size=int(sys.argv[3]),
         optimizer=sys.argv[4],
         loss=LOSS[int(sys.argv[5]) - 1][1],
         metrics=METRICS)

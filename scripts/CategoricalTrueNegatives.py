import numpy as np
from numpy import random as random
import tensorflow as tf
import keras
import keras.backend as K


class CategoricalTrueNegatives(tf.keras.metrics.Metric):

    def __init__(self, num_classes, batch_size,
                 name="categorical_true_negatives", **kwargs):
        super(CategoricalTrueNegatives, self).__init__(name=name, **kwargs)

        self.batch_size = batch_size
        self.num_classes = num_classes

        self.cat_true_negatives = self.add_weight(name="ctn", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):

        y_true = K.argmax(y_true, axis=-1)
        y_pred = K.argmax(y_pred, axis=-1)
        y_true = K.flatten(y_true)

        true_neg = K.sum(K.cast((K.not_equal(y_true, y_pred)), dtype=tf.float32))

        self.cat_true_negatives.assign_add(true_neg)

    def result(self):

        return self.cat_true_negatives

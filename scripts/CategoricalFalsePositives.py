import numpy as np
from numpy import random as random
import tensorflow as tf
import keras
import keras.backend as K


class CategoricalFalsePositives(tf.keras.metrics.Metric):

    def __init__(self, num_classes, batch_size,
                 name="categorical_false_positives", **kwargs):
        super(CategoricalFalsePositives, self).__init__(name=name, **kwargs)

        self.batch_size = batch_size
        self.num_classes = num_classes

        self.cat_false_positives = self.add_weight(name="cfp", initializer="zeros")

    def update_state(self, y_false, y_pred, sample_weight=None):

        y_false = K.argmin(y_false, axis=-1)
        y_pred = K.argmin(y_pred, axis=-1)
        y_false = K.flatten(y_false)

        false_poss = K.sum(K.cast((K.equal(y_false, y_pred)), dtype=tf.float32))

        self.cat_false_positives.assign_add(false_poss)

    def result(self):

        return self.cat_false_positives

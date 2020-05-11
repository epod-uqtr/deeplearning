import os
import subprocess

import tensorflow as tf
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from trainingsession.forms import TrainingSessionForm
from trainingsession.models import TrainingSession

OPTIMIZERS = [
    (1, tf.keras.optimizers.Adadelta(), 'Adadelta'),
    (2, tf.keras.optimizers.Adagrad(), 'Adagrad'),
    (3, tf.keras.optimizers.Adam(), 'Adam'),
    (4, tf.keras.optimizers.Adamax(), 'Adamax'),
    (5, tf.keras.optimizers.Ftrl(), 'FTRL'),
    (6, tf.keras.optimizers.Nadam(), 'NAdam'),
    (7, tf.keras.optimizers.RMSprop(), 'RMSprop'),
    (8, tf.keras.optimizers.SGD(), 'SGD'),
]
LOSS = [
    (1, tf.keras.losses.BinaryCrossentropy(), 'Binary crossentropy'),
    (2, tf.keras.losses.CategoricalCrossentropy(), 'Categorical crossentropy'),
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
METRICS = [
    (1, 'accuracy', 'Accuracy'),
]


@login_required(login_url='/login/')
def index(request, session_name):
    print("--- " + str(session_name))
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, request.FILES)
        if form.is_valid():
            epochs = form.cleaned_data['epochs']
            batch_size = form.cleaned_data['batch_size']
            optimizer = form.cleaned_data['optimizer']
            loss = form.cleaned_data['loss']
            metrics = form.cleaned_data['metrics']
            print("+++ " + str(session_name))
            print("+++epochs " + str(epochs))
            print("+++batch_size " + str(batch_size))
            print("+++optimizer " + str(optimizer))
            print("+++loss " + str(loss))
            print("+++loss " + str(LOSS[int(loss) - 1][1].name))
            print("+++metrics " + str(metrics))
            instance = TrainingSession.objects.create(session_name=session_name,
                                                      state=False,
                                                      type=form.cleaned_data['type'],
                                                      script=request.FILES['script'],
                                                      searcher=request.user,
                                                      epochs=epochs,
                                                      batch_size=batch_size,
                                                      optimizer=OPTIMIZERS[int(optimizer) - 1][2],
                                                      loss=LOSS[int(loss) - 1][2],
                                                      metrics=METRICS[int(metrics) - 1][2])
            metr = []
            metr.append(METRICS[int(metrics) - 1][1])
            exec_script(instance, session_name, int(epochs), int(batch_size), OPTIMIZERS[int(optimizer) - 1][2],
                        LOSS[int(loss) - 1][1].name, METRICS[int(metrics) - 1][1])
            TrainingSession.objects.filter(pk=instance.pk).update(state=True)

        return render(request, 'trainingsession/report.html', {
            'session_name': session_name
        })
    else:
        form = TrainingSessionForm()
        return render(request, 'trainingsession/index.html', {
            'form': form
        })


def report(request):
    pass


def exec_script(instance, session_name, epochs, batch_size, optimizer, loss, metrics):
    script_path = os.path.join('/home/lacen/PycharmProjects/deeplearning', str(instance.script))
    subprocess.call(["python", script_path,
                     str(session_name),
                     str(epochs),
                     str(batch_size),
                     str(optimizer),
                     str(loss),
                     str(metrics)])

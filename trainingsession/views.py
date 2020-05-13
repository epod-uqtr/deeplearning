import os
import subprocess

import keras
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from trainingsession.forms import TrainingSessionForm
from trainingsession.models import TrainingSession

OPTIMIZERS = [
    (1, keras.optimizers.Adadelta(), 'Adadelta'),
    (2, keras.optimizers.Adagrad(), 'Adagrad'),
    (3,  keras.optimizers.Adam(), 'Adam'),
    (4,  keras.optimizers.Adamax(), 'Adamax'),
    (6,  keras.optimizers.Nadam(), 'NAdam'),
    (6,  keras.optimizers.Nadam(), 'NAdam'),
    (7,  keras.optimizers.RMSprop(), 'RMSprop'),
    (8,  keras.optimizers.SGD(), 'SGD'),
]
LOSS = [
    (1, keras.losses.BinaryCrossentropy(), 'Binary crossentropy'),
    (2, keras.losses.CategoricalCrossentropy(), 'Categorical crossentropy'),
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
            print("+++ " + str(session_name))
            print("+++epochs " + str(epochs))
            print("+++batch_size " + str(batch_size))
            print("+++optimizer " + str(optimizer))
            print("+++loss " + str(loss))
            print("+++loss " + str(LOSS[int(loss) - 1][1].name))
            instance = TrainingSession.objects.create(session_name=session_name,
                                                      state=False,
                                                      type=form.cleaned_data['type'],
                                                      script=request.FILES['script'],
                                                      searcher=request.user,
                                                      epochs=epochs,
                                                      batch_size=batch_size,
                                                      optimizer=OPTIMIZERS[int(optimizer) - 1][2],
                                                      loss=LOSS[int(loss) - 1][2])
            exec_script(instance, session_name, int(epochs), int(batch_size), OPTIMIZERS[int(optimizer) - 1][2],
                            LOSS[int(loss) - 1][0])

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


def exec_script(instance, session_name, epochs, batch_size, optimizer, loss):
    script_path = os.path.join('/home/lacen/PycharmProjects/deeplearning', str(instance.script))
    return subprocess.call(["python", script_path,
                            str(session_name),
                            str(epochs),
                            str(batch_size),
                            str(optimizer),
                            str(loss)])

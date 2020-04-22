import os
import subprocess
from subprocess import Popen

from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

import shlex
from trainingsession.forms import TrainingSessionForm
from trainingsession.models import TrainingSession


def index(request):
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = TrainingSession(state='In progress',
                                       type=form.cleaned_data['type'],
                                       script=request.FILES['script'])
            instance.save()
    else:
        form = TrainingSessionForm()
    return render(request, 'trainingsession/index.html', {
        'form': form
    })


@receiver(post_save, sender=TrainingSession)
def my_callback(sender, instance, created, **kwargs):
    if created:
        script_path = os.path.join('/home/lacen/PycharmProjects/deeplearning', str(instance.script))
        print(str(instance.date_created))
        subprocess.call(["python", script_path, str(instance.date_created_on_ms)])
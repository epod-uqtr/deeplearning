import asyncio
import json
import os
import subprocess
import uuid
from subprocess import Popen

from asgiref.sync import async_to_sync, AsyncToSync
from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

import shlex
from trainingsession.forms import TrainingSessionForm
from trainingsession.models import TrainingSession
from channels.layers import get_channel_layer


def index(request, session_name):
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = TrainingSession(state='In progress',
                                       type=form.cleaned_data['type'],
                                       script=request.FILES['script'])
            channel_layer = get_channel_layer()
            print("+++ " + str(session_name))
            async_to_sync(channel_layer.group_add)(session_name, session_name)
            instance.save()
            exec_script(instance, session_name)

        return HttpResponse('<h1>Report</h1>')
    else:
        form = TrainingSessionForm()
        return render(request, 'trainingsession/index.html', {
            'form': form
        })


def report(request):
    pass


def exec_script(instance, session_name):
    script_path = os.path.join('/home/lacen/PycharmProjects/deeplearning', str(instance.script))
    subprocess.call(["python", script_path, str(session_name)])

import uuid

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from trainingsession.models import TrainingSession


def index(request):
    pass


class TrainingSessionListView(ListView):
    model = TrainingSession
    template_name = 'dashboard/index.html'
    context_object_name = 'training_sessions'
    ordering = ['date_created']

    def get_context_data(self, **kwargs):
        context = super(TrainingSessionListView, self).get_context_data(**kwargs)
        context['session_name'] = uuid.uuid4().hex
        return context


class TrainingSessionDetailView(DetailView):
    model = TrainingSession
    template_name = 'dashboard/trainingsession_detail.html'
    context_object_name = 'training_session'

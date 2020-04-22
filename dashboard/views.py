from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from trainingsession.models import TrainingSession


def index(request):
    context = {
        'training_sessions': TrainingSession.objects.all()
    }
    return render(request, 'dashboard/index.html', context)


class TrainingSessionListView(ListView):
    model = TrainingSession
    template_name = 'dashboard/index.html'
    context_object_name = 'training_sessions'
    ordering = ['date_created']


class TrainingSessionDetailView(DetailView):
    model = TrainingSession
    template_name = 'dashboard/trainingsession_detail.html'
    context_object_name = 'training_session'

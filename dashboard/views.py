import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from trainingsession.models import TrainingSession


class TrainingSessionListView(ListView):
    model = TrainingSession
    template_name = 'dashboard/index.html'
    context_object_name = 'training_sessions'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super(TrainingSessionListView, self).get_context_data(**kwargs)
        context['session_name'] = uuid.uuid4().hex
        context['sessions_number'] = self.get_queryset().count()
        return context

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(TrainingSessionListView, self).get_queryset()
        queryset = queryset.filter(searcher=self.request.user)
        return queryset


class TrainingSessionDetailView(DetailView):
    model = TrainingSession
    template_name = 'dashboard/trainingsession_detail.html'
    context_object_name = 'training_session'
    slug_field = "session_name"
    slug_url_kwarg = "session_name"

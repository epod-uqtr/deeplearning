from django import forms
from django.forms import TextInput, FileInput

from trainingsession.models import TrainingSession


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['type', 'script']

    def __init__(self, *args, **kwargs):
        super(TrainingSessionForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = TextInput(attrs={
            'label': 'Type',
            'type': 'text',
            'class': 'form-control mb-3',
            'name': 'type',
            'placeholder': 'eg. RNN'})
        self.fields['script'].widget = FileInput(attrs={
            'type': 'file',
            'class': 'form-control-file',
            'name': 'script',
            'data-url': "{% url 'photos:basic_upload' %}",
            'data-form-data': '{"csrfmiddlewaretoken": "{{ csrf_token }}"}'})

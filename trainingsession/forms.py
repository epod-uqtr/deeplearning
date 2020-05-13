import uuid

from django import forms
from django.forms import TextInput, FileInput, Select, MultipleChoiceField, ModelChoiceField

from trainingsession.models import TrainingSession

OPTIMIZERS = [
    (1, 'Adadelta'),
    (2, 'Adagrad'),
    (3, 'Adam'),
    (4, 'Adamax'),
    (6, 'NAdam'),
    (6, 'NAdam'),
    (7, 'RMSprop'),
    (8, 'SGD'),
]
LOSS = [
    (1, 'Binary crossentropy'),
    (2, 'Categorical crossentropy'),
    (3, 'Categorical hinge'),
    (5, 'Hinge'),
    (5, 'Hinge'),
    (6, 'Huber'),
    (7, 'Squared hinge'),
    (8, 'Hyperbolic Cosine'),
    (9, 'Mean absolute error'),
    (10, 'Mean absolute percentage error'),
    (11, 'Mean squared error'),
    (12, 'Mean squared logarithmic error (MSLE)'),
    (13, 'Poisson'),
    (14, 'Sparse categorical crossentropy'),
]
# METRICS = [
#   keras.metrics.TruePositives(name='tp'),
#   keras.metrics.FalsePositives(name='fp'),
#   keras.metrics.TrueNegatives(name='tn'),
#   keras.metrics.FalseNegatives(name='fn'),
#   keras.metrics.Precision(name='precision'),
#   keras.metrics.Recall(name='recall'),
#   keras.metrics.CategoricalAccuracy(name='acc'),
#   keras.metrics.AUC(name='auc'),
# ]
METRICS = [
    (1, 'Accuracy'),
]


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['type', 'script', 'epochs', 'batch_size', 'optimizer', 'loss']

    def __init__(self, *args, **kwargs):
        super(TrainingSessionForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = TextInput(attrs={
            'label': 'Type',
            'type': 'text',
            'class': 'form-control mb-3',
            'name': 'type',
            'placeholder': 'Model name'})
        self.fields['script'].widget = FileInput(attrs={
            'type': 'file',
            'class': 'form-control-file',
            'name': 'script',
            'data-url': "{% url 'photos:basic_upload' %}",
            'data-form-data': '{"csrfmiddlewaretoken": "{{ csrf_token }}"}'})
        self.fields['epochs'].widget = TextInput(attrs={
            'label': 'Type',
            'type': 'text',
            'class': 'form-control',
            'name': 'type',
            'placeholder': '30',
            'aria-label': 'epochs',
            'aria-describedby': 'addon-wrapping'})
        self.fields['batch_size'].widget = TextInput(attrs={
            'label': 'Type',
            'type': 'text',
            'class': 'form-control',
            'name': 'type',
            'placeholder': '64',
            'aria-label': 'batch_size',
            'aria-describedby': 'addon-wrapping'})
        self.fields['optimizer'].widget = Select(attrs={'class': 'form-control'}, choices=OPTIMIZERS)
        self.fields['loss'].widget = Select(attrs={'class': 'form-control'}, choices=LOSS)

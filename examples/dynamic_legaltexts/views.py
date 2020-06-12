from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import ParticipationForm
from .models import Survey


class DynamicParticipantFormView(CreateView):
    template_name = 'form.html'
    form_class = ParticipationForm
    success_url = reverse_lazy('dynamic-form-completed')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['survey'] = get_object_or_404(Survey, pk=self.kwargs['id'])
        return kwargs


class DynamicParticipantCompletedView(TemplateView):
    template_name = 'form-completed.html'

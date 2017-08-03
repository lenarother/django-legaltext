from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import ParticipationForm


class StaticParticipantFormView(CreateView):
    template_name = 'form.html'
    form_class = ParticipationForm
    success_url = reverse_lazy('static-form-completed')


class StaticParticipantCompletedView(TemplateView):
    template_name = 'form-completed.html'

from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView

from .forms import MockappParticipationForm


class MockappParticipantFormView(FormView):
    form_class = MockappParticipationForm
    template_name = 'mockapp/form.html'

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(MockappParticipantFormView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('form-completed', kwargs=self.kwargs)


class MockappParticipantCompletedView(TemplateView):
    permanent = False
    template_name = 'mockapp/form-completed.html'

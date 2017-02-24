from django.http import Http404
from django.views.generic import TemplateView

from .models import LegalText


class LegaltextView(TemplateView):
    permanent = False
    template_name = 'legaltext/content.html'

    def get_context_data(self, **kwargs):
        context = super(LegaltextView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']

        try:
            legaltext = LegalText.objects.get(slug=slug)
            legaltext_version = legaltext.get_current_version()
        except LegalText.DoesNotExist:
            raise Http404

        context.update({'current_version': legaltext_version})
        context.update({'current_version_content': legaltext_version.get_content()})

        return context

from django.views.generic import TemplateView

from .models import LegalText


class LegaltextView(TemplateView):
    permanent = False
    template_name = 'legaltext/content.html'

    def get_context_data(self, **kwargs):
        context = super(LegaltextView, self).get_context_data(**kwargs)
        try:
            slug = self.kwargs['slug']
        except KeyError:
            slug = 'default'

        legaltext_version = LegalText.current_version(slug)
        context.update({'current_version': legaltext_version})
        context.update({'current_version_content': legaltext_version.get_content()})

        return context

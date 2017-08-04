from django.conf import settings
from django.views.generic import DetailView

from .models import LegalText


class LegaltextView(DetailView):
    model = LegalText

    def get_template_names(self):
        template_name = getattr(
            settings, 'LEGALTEXT_VIEW_TEMPLATE', 'legaltext/content.html')
        overrides = getattr(settings, 'LEGALTEXT_VIEW_TEMPLATE_OVERRIDES', {})
        return overrides.get(self.object.slug, template_name)

    def get_context_data(self, **kwargs):
        context = super(LegaltextView, self).get_context_data(**kwargs)

        legaltext_version = self.object.get_current_version()
        context.update({
            'current_version': legaltext_version,
            'current_version_content': legaltext_version.render_content()
        })
        return context

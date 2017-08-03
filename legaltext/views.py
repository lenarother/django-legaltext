from django.views.generic import DetailView

from .models import LegalText


class LegaltextView(DetailView):
    template_name = 'legaltext/content.html'
    model = LegalText

    def get_context_data(self, **kwargs):
        context = super(LegaltextView, self).get_context_data(**kwargs)

        legaltext_version = self.object.get_current_version()
        context.update({
            'current_version': legaltext_version,
            'current_version_content': legaltext_version.render_content()
        })
        return context

from django.db import models
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .models import LegalText


class LegalTextContent(models.Model):
    legaltext = models.ForeignKey(LegalText, verbose_name=_('Legal text'))

    class Meta:
        abstract = True
        verbose_name = _('Legal text')
        verbose_name_plural = _('Legal texts')

    def render(self, request, *args, **kwargs):
        context = kwargs.get('context') or RequestContext(request)
        context['current_version'] = self.legaltext.current_version
        return render_to_string('legaltext/content.html', context_instance=context)

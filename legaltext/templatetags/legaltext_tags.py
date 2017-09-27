from django import template
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from ..models import LegalText


register = template.Library()


@register.simple_tag(takes_context=True)
def legaltext_url(context, name):
    legaltext = LegalText.objects.filter(Q(url_name=name) | Q(slug=name)).first()
    silent = getattr(settings, 'LEGALTEXT_SILENCE_TEMPLATE_ERRORS', False)
    if not legaltext:
        if silent:
            return ''
        raise NoReverseMatch(_('Legaltext with slug/name: {0} does not exist').format(name))
    return legaltext.get_absolute_url()

from django import template
from django.db.models import Q

from ..models import LegalText

register = template.Library()


@register.simple_tag(takes_context=True)
def legaltext_url(context, name):
    legaltext = LegalText.objects.filter(Q(url_name=name) | Q(slug=name)).first()
    if not legaltext:
        return ''
    return legaltext.get_absolute_url()

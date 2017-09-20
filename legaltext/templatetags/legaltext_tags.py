from django import template
from django.db.models import Q
# from django.core.exceptions import NoReverseMatch
from django.urls.exceptions import NoReverseMatch
from django.utils.html import conditional_escape
from django.utils.translation import ugettext_lazy as _

from ..models import LegalText

register = template.Library()


class LegaltextURLNode(template.base.Node):
    def __init__(self, legaltext_slug_or_name, asvar):
        self.legaltext_slug_or_name = legaltext_slug_or_name
        self.asvar = asvar

    def render(self, context):
        legaltext_slug_or_name = self.legaltext_slug_or_name.resolve(context)
        legaltext = LegalText.objects.filter(
            Q(slug=legaltext_slug_or_name) | Q(url_name=legaltext_slug_or_name)).first()

        url = ''
        if legaltext:
            url = legaltext.get_absolute_url()
        if not legaltext and self.asvar is None:
            raise NoReverseMatch(
                _('No legaltext with slug or url_name: "{0}"').format(legaltext_slug_or_name))

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            if context.autoescape:
                url = conditional_escape(url)
            return url


@register.tag
def legaltext_url(parser, token):
    bits = token.split_contents()
    if len(bits) < 2 or bits[1] == 'as':
        raise template.base.TemplateSyntaxError(
            '{0} takes at least one argument, the name or slug of a '
            'legaltext.'.format(bits[0]))
    legaltext_slug_or_name = parser.compile_filter(bits[1])
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits) == 1 or (len(bits)) >= 2 and bits[-2] != 'as':
        raise template.base.TemplateSyntaxError('Malformed arguments to legaltext_url tag')

    return LegaltextURLNode(legaltext_slug_or_name, asvar)

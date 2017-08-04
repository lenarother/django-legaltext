import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from markymark.fields import MarkdownField
from markymark.utils import render_markdown


ANCHOR_RE = re.compile('\[anchor(?:\:([^\]]+))?\](?:(.+?)\[/anchor\])')
BLOCK_RE = re.compile('\[block\:([^\]]+)\](?:(.+?)\[/block\])', re.DOTALL)


class LegalText(models.Model):
    name = models.CharField(_('Legal text'), max_length=64)
    slug = models.SlugField(_('Slug'), max_length=64, unique=True)

    class Meta:
        verbose_name = _('Legal text')
        verbose_name_plural = _('Legal texts')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @classmethod
    def current_version(cls, slug):
        obj, created = LegalText.objects.get_or_create(
            slug=slug, defaults={'name': slug})
        return obj.get_current_version()

    def get_current_version(self):
        version = self.legaltextversion_set.filter(
            valid_from__lte=timezone.now()).first()
        if version:
            return version
        return LegalTextVersion.objects.get_or_create(legaltext=self)[0]


class LegalTextVersion(models.Model):
    legaltext = models.ForeignKey(LegalText, verbose_name=_('Legal text'))
    valid_from = models.DateTimeField(_('Valid from'), default=timezone.now)

    content = MarkdownField(_('Text'), help_text=_(
        'You can use [block:foo]Your text[/block] to create a block with an anchor. '
        'Anchors ([anchor:foo]) can be used in checkbox texts to link to '
        'specific parts of the legal text.'
    ))

    class Meta:
        verbose_name = _('Legal text version')
        verbose_name_plural = _('Legal text versions')
        ordering = ('legaltext__slug', '-valid_from')

    def __str__(self):
        return '{0} ({1:%x %X})'.format(
            self.legaltext.name, timezone.localtime(self.valid_from))

    @property
    def name(self):
        return self.legaltext.name

    def render_content(self):
        anchor_class = getattr(settings, 'LEGALTEXT_ANCHOR_CLASS', None)

        def block_callback(match):
            return (
                '<div class="legaltext-block legaltext-block-{0}">'
                '<span id="{0}"{1}></span>{2}</div>'
            ).format(
                match.group(1),
                ' class="{0}"'.format(anchor_class) if anchor_class else '',
                render_markdown(match.group(2))
            )

        content = BLOCK_RE.sub(block_callback, self.content)
        return render_markdown(content)


class LegalTextCheckbox(models.Model):
    legaltext_version = models.ForeignKey(
        LegalTextVersion, verbose_name=_('Legal text version'), related_name='checkboxes')

    content = MarkdownField(_('Text'), help_text=_(
        'You can use [anchor]Your text[/anchor] to create a link to the full legal text. '
        'If you use [anchor:foo]Your text[/anchor] the link will go to the block "foo" '
        'inside the legal text.'
    ))

    class Meta:
        verbose_name = _('Legal text checkbox')
        verbose_name_plural = _('Legal text Checkboxes')
        ordering = ('legaltext_version',)

    def __str__(self):
        return ugettext('Checkbox for {0} ({1})').format(
            self.legaltext_version.name,
            '{0:%x %X}'.format(timezone.localtime(self.legaltext_version.valid_from))
        )

    def render_content(self):
        def anchor_callback(match):
            return '<a href="{0}{1}" class="legaltext-anchor" target="_blank">{2}</a>'.format(
                reverse('legaltext', args=(self.legaltext_version.legaltext.slug,)),
                '#{0}'.format(match.group(1)) if match.group(1) else '',
                match.group(2)
            )

        content = ANCHOR_RE.sub(anchor_callback, self.content)
        return render_markdown(content).replace('<p>', '').replace('</p>', '')

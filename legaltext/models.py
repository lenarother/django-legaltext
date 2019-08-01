import re

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import normalize_newlines
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from markymark.fields import MarkdownField
from markymark.utils import render_markdown


ANCHOR_RE = re.compile('\[anchor(?:\:([^\]]+))?\](?:(.+?)\[/anchor\])')
BLOCK_OPEN_NL_RE = re.compile('(?:\n\n|\n)?(\[block\:[^\]]+\])(?:\n\n|\n)?', re.DOTALL)
BLOCK_CLOSE_NL_RE = re.compile('(?:\n\n|\n)?(\[/block\])(?:\n\n|\n)?', re.DOTALL)
BLOCK_OPEN_RE = re.compile('(?:<p>)?\[block\:([^\]]+)\](?:</p>)?')
BLOCK_CLOSE_RE = re.compile('(?:<p>)?\[/block\](?:</p>)?')


class LegalText(models.Model):
    name = models.CharField(_('Legal text'), max_length=64)
    slug = models.SlugField(_('Slug'), max_length=128, unique=True)
    url_name = models.SlugField(
        _('URL Name'), max_length=128, unique=True, blank=True, null=True, help_text=_(
            'Optional URL name for the legal text. If not provided, the slug is used.'))

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
        if not version:
            version, created = LegalTextVersion.objects.get_or_create(legaltext=self)
            if created:
                version.checkboxes.create(content=ugettext('I accept.'))

        return version

    def get_absolute_url(self):
        return reverse('legaltext', args=(self.url_name or self.slug,))


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

        def block_nl_callback(match):
            return '\n\n{0}\n\n'.format(match.group(1))

        def block_open_callback(match):
            block_open_callback.count += 1
            return (
                '<div class="legaltext-block legaltext-block-{0}">'
                '<span id="{0}"{1}></span>'
            ).format(
                match.group(1),
                ' class="{0}"'.format(anchor_class) if anchor_class else '',
            )
        block_open_callback.count = 0

        def block_close_callback(match):
            block_close_callback.count += 1
            return '</div>'
        block_close_callback.count = 0

        content = BLOCK_OPEN_NL_RE.sub(block_nl_callback, self.content)
        content = BLOCK_CLOSE_NL_RE.sub(block_nl_callback, content)

        content = render_markdown(content)
        content = BLOCK_OPEN_RE.sub(block_open_callback, content)
        content = BLOCK_CLOSE_RE.sub(block_close_callback, content)

        if block_open_callback.count == block_close_callback.count:
            return content
        return render_markdown(self.content)


class LegalTextCheckbox(models.Model):
    legaltext_version = models.ForeignKey(
        LegalTextVersion, verbose_name=_('Legal text version'), related_name='checkboxes')

    content = MarkdownField(_('Text'), help_text=_(
        'You can use [anchor]Your text[/anchor] to create a link to the full legal text. '
        'If you use [anchor:foo]Your text[/anchor] the link will go to the block "foo" '
        'inside the legal text.'
    ))
    order = models.PositiveIntegerField(_('Order'), blank=True, null=True)

    class Meta:
        verbose_name = _('Legal text checkbox')
        verbose_name_plural = _('Legal text Checkboxes')
        ordering = ('legaltext_version', 'order')
        unique_together = (('legaltext_version', 'order'),)

    def __str__(self):
        return ugettext('Checkbox for {0} ({1})').format(
            self.legaltext_version.name,
            '{0:%x %X}'.format(timezone.localtime(self.legaltext_version.valid_from))
        )

    def render_content(self):
        def anchor_callback(match):
            return '<a href="{0}{1}" class="legaltext-anchor" target="_blank">{2}</a>'.format(
                self.legaltext_version.legaltext.get_absolute_url(),
                '#{0}'.format(match.group(1)) if match.group(1) else '',
                match.group(2)
            )

        content = ANCHOR_RE.sub(
            anchor_callback,
            normalize_newlines(self.content).replace('\n', '<br />')
        )
        return render_markdown(content).replace('<p>', '').replace('</p>', '')

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = (self.legaltext_version.checkboxes.aggregate(
                next_order=models.Max('order'))['next_order'] or 0) + 1
        super(LegalTextCheckbox, self).save(*args, **kwargs)

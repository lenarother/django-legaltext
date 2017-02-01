from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _

from markymark.fields import MarkdownField


class LegalText(models.Model):
    name = models.CharField(_('Legal text'), max_length=64, unique=True)
    slug = models.SlugField(_('Slug'), max_length=64, unique=True)

    class Meta:
        verbose_name = _('Legal text')
        verbose_name_plural = _('Legal texts')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @classmethod
    def current(cls, slug):
        obj, created = LegalText.objects.get_or_create(
            slug=slug, defaults={'name': slug})
        return obj.current_version

    @property
    def current_version(self):
        versions = list(self.legaltextversion_set.all()[:1])
        if versions:
            return versions[0]
        obj, created = LegalTextVersion.objects.get_or_create(legaltext=self)
        return obj

    @property
    def current_content(self):
        return self.current_version.content


class LegalTextVersion(models.Model):
    legaltext = models.ForeignKey(LegalText, verbose_name=_('Legal text'),)
    valid_from = models.DateTimeField(_('Valid from'), default=timezone.now)
    content = MarkdownField(_('Text'))
    checkbox_text = MarkdownField(_('Checkbox Text'))

    class Meta:
        verbose_name = _('Legal text version')
        verbose_name_plural = _('Legal text versions')
        ordering = ('legaltext__name', '-valid_from')

    def __str__(self):
        return '%s (%s)' % (self.legaltext.name, self.valid_from_display)

    @property
    def valid_from_display(self):
        return str(localtime(self.valid_from).strftime('%Y-%m-%d %H:%M'))

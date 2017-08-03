from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from markymark.fields import MarkdownField


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

    content = MarkdownField(_('Text'))

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
        # TODO: Insert anchors
        return self.content


class LegalTextCheckbox(models.Model):
    legaltext_version = models.ForeignKey(
        LegalTextVersion, verbose_name=_('Legal text version'), related_name='checkboxes')

    content = MarkdownField(_('Text'))

    class Meta:
        verbose_name = _('Legal text checkbox')
        verbose_name_plural = _('Legal text Checkboxes')
        ordering = ('legaltext_version',)

    def __str__(self):
        return ugettext('Checkbox for {0} ({1:%x %X})').format(
            self.legaltext_version.name,
            timezone.localtime(self.legaltext_version.valid_from)
        )

    def render_content(self):
        # TODO: Insert links
        return self.content

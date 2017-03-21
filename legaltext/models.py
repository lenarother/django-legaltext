import re

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

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
    legaltext = models.ForeignKey(LegalText, verbose_name=_('Legal text'),)
    valid_from = models.DateTimeField(_('Valid from'), default=timezone.now)

    content = MarkdownField(_('Text'), help_text=_(
        'Optional: use [[checkbox-anchor-name]] text ... [[end]] to insert checkbox anchor'))

    class Meta:
        verbose_name = _('Legal text version')
        verbose_name_plural = _('Legal text versions')
        ordering = ('legaltext__slug', '-valid_from')

    def __str__(self):
        return '{0} ({1:%x %X})'.format(
            self.legaltext.name, timezone.localtime(self.valid_from))

    def get_content(self):
        """
        Changes [[anchor]] and [[end]] keywords into div

        Returns:
            legaltext text including formatting as string

        """
        legaltext_content = re.sub(
            '\[\[end\]\]',
            '</div>',
            self.content
        )

        legaltext_content = re.sub(
            '\[\[(.*)\]\]',
            '<div class="\g<1>"><span class="anchor" id="\g<1>"></span>',
            legaltext_content
        )

        return legaltext_content


class CheckboxTextVersion(models.Model):
    legaltext_version = models.ForeignKey(
        LegalTextVersion, verbose_name=_('Legal text version'),)

    content = MarkdownField(_('Text'), help_text=_(
        'Use [[word]] to indicate the word used as a link to the legaltext content.'))
    anchor = models.CharField(_('Anchor'), max_length=64, blank=True)

    class Meta:
        verbose_name = _('Checkbox')
        verbose_name_plural = _('Checkboxes')
        ordering = ('legaltext_version',)

    def __str__(self):
        name = 'Checkbox'
        if self.anchor:
            name += ' (with {0} anchor)'.format(self.anchor)
        return '{0} for {1} ({2:%x %X})'.format(
            name, self.legaltext_version.legaltext.name,
            timezone.localtime(self.legaltext_version.valid_from))

    @property
    def slug(self):
        return self.legaltext_version.legaltext.slug

    def get_content(self, privacy=False):
        """
        Includes url to legaltext in checkbox content text
        Uses word in squer brackets e.g. [[privacy terms]]

        Returns:
            checkbox lablel as string contailing url

        """
        legaltext_url = reverse('legaltext', kwargs={'slug': self.slug})
        if self.anchor:
            legaltext_url += '#{0}'.format(self.anchor)

        return re.sub(
            '\[\[(.*)\]\]',
            '<a href="{0}" title="\g<1>">\g<1></a>'.format(legaltext_url),
            self.content
        )

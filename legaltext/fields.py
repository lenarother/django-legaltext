from django.db import models
from django.utils.deconstruct import deconstructible

from .models import LegalText, LegalTextVersion


@deconstructible
class CurrentLegalText(object):

    def __init__(self, slug):
        self.slug = slug

    def __call__(self):
        return LegalText.current_version(self.slug)


class LegalTextField(models.ForeignKey):

    def __init__(self, slug=None, to=LegalTextVersion, **kwargs):
        self.slug = slug
        kwargs['default'] = CurrentLegalText(slug)
        kwargs['limit_choices_to'] = {'legaltext__slug': slug}
        kwargs['related_name'] = '+'
        kwargs['blank'] = True
        kwargs['null'] = True
        super(LegalTextField, self).__init__(to, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(LegalTextField, self).deconstruct()
        kwargs['slug'] = self.slug
        return name, path, args, kwargs

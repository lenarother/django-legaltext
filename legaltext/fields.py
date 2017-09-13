import floppyforms.__future__ as forms
from django.db import models
from django.utils.deconstruct import deconstructible

from .models import LegalText, LegalTextVersion
from .widgets import LegalTextWidget


@deconstructible
class CurrentLegalText(object):

    def __init__(self, slug):
        self.slug = slug

    def __call__(self):
        return LegalText.current_version(self.slug).pk


class LegalTextField(models.ForeignKey):

    def __init__(self, slug=None, to=LegalTextVersion, **kwargs):
        self.slug = slug
        if slug:
            kwargs.setdefault('default', CurrentLegalText(slug))
            kwargs['limit_choices_to'] = {'legaltext__slug': slug}
        kwargs['related_name'] = '+'
        kwargs['blank'] = True
        kwargs['null'] = True
        super(LegalTextField, self).__init__(to, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(LegalTextField, self).deconstruct()
        kwargs['slug'] = self.slug
        return name, path, args, kwargs


class LegalTextFormField(forms.BooleanField):

    def __init__(self, slug, *args, **kwargs):
        self.slug = slug
        kwargs.setdefault('widget', LegalTextWidget(self.slug))
        kwargs.setdefault('required', True)
        super(LegalTextFormField, self).__init__(*args, **kwargs)

    label = property(lambda s: LegalText.current_version(s.slug).name, lambda s, v: None)

    def prepare_value(self, value):
        return bool(value)

    def to_python(self, value):
        if not value or value in self.empty_values:
            return None
        return LegalText.current_version(self.slug)

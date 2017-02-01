from django import forms
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.safestring import mark_safe

from .models import LegalText, LegalTextVersion


@deconstructible
class CurrentLegalText(object):

    def __init__(self, slug):
        self.slug = slug

    def __call__(self):
        return LegalText.current_version(self.slug)


class LegalTextFormField(forms.BooleanField):

    def __init__(self, slug, *args, **kwargs):
        self.slug = slug
        super().__init__(*args, **kwargs)

    label = property(
        lambda s: mark_safe(LegalText.current_version(s.slug).checkbox_label),
        lambda s, v: v
    )

    def prepare_value(self, value):
        return bool(value)

    def to_python(self, value):
        if not value or value in self.empty_values:
            return None
        return LegalText.current_version(self.slug)


class LegalTextField(models.ForeignKey):

    def __init__(self, slug=None, to=LegalTextVersion, **kwargs):
        self.slug = slug
        kwargs['default'] = CurrentLegalText(slug)
        kwargs['limit_choices_to'] = {'legaltext__slug': slug}
        kwargs['related_name'] = '+'
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['slug'] = self.slug
        return name, path, args, kwargs

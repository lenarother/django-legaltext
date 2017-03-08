from django import forms
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.safestring import mark_safe

from .models import LegalText, LegalTextVersion


def add_legaltext_checkboxes(fields, slug):
    """
    Fetch current version of legal text with given slug
    Adds all its checkboxes to formular fields

    Args:
        formular fields (self.fields in form __init__)
        legal text slug
    """
    version = LegalText.current_version(slug)
    for counter, checkbox in enumerate(version.checkboxtextversion_set.all()):
        field_name = 'Checkbox_{}_{}'.format(counter, version.pk)
        fields[field_name] = LegalTextCheckboxFormField(checkbox)


@deconstructible
class CurrentLegalText(object):

    def __init__(self, slug):
        self.slug = slug

    def __call__(self):
        return LegalText.current_version(self.slug)


class LegalTextCheckboxFormField(forms.BooleanField):

    def __init__(self, checkbox, *args, **kwargs):
        self.checkbox = checkbox
        super().__init__(*args, **kwargs)

    label = property(
        lambda s: mark_safe(s.checkbox.get_content()),
        lambda s, v: v
    )

    def prepare_value(self, value):
        return bool(value)

    def to_python(self, value):
        if not value or value in self.empty_values:
            return None
        return bool(value)


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

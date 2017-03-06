import pickle
from django import forms
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

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
        return self.checkbox


class MultipleCheckboxWidget(forms.widgets.MultiWidget):

    def __init__(self, checkboxes, attrs=None):
        self.checkboxes = checkboxes
        widgets = [forms.CheckboxInput() for checkbox in checkboxes]
        super(MultipleCheckboxWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        # import ipdb; ipdb.set_trace()

        for key in data:
            if key.startswith(name):
                if data[key][0] != 'on':
                    return False
        return True

    def decompress(self, value):
        import ipdb; ipdb.set_trace()
        if value:
            return pickle.loads(value)
        else:
            return ['', '']

    def format_output(self, rendered_widgets):
        # This will work until django 1.10.
        # In django 1.11 format_output is removed
        # https://docs.djangoproject.com/en/dev/releases/1.11/
        result = ''
        for x, y in zip(rendered_widgets, self.checkboxes):
            result += u'<p class="placewidget">%s %s</p>' % (
                x, y.get_content())
        return mark_safe(result)


class MultiCheckboxFormField(forms.fields.MultiValueField):

    def __init__(self, slug=None, to=LegalTextVersion, **kwargs):
        error_messages = {'incomplete': _('This field is required')}
        text = LegalText.current_version(slug)
        checkboxes = text.checkboxtextversion_set.all()
        fields_list = [forms.BooleanField() for checkbox in checkboxes]
        fields = tuple(fields_list)
        self.widget = MultipleCheckboxWidget(checkboxes)
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=True, **kwargs)

    def compress(self, data_list):
        return all(x is True for x in data_list)


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

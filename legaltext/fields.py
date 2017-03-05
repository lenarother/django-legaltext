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

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '']

    # def format_output(self, rendered_widgets):
    #     return ''.join(rendered_widgets)

    def format_output(self, rendered_widgets):
        # import ipdb; ipdb.set_trace()
        return mark_safe(u'<p class="placewidget">%s <br />%s</p>' % (
            rendered_widgets[0], 'tralala'
           
        ))


class CheckboxFormField(forms.fields.MultiValueField):
    #widget = MultipleCheckboxWidget
    # label = property(
    #     lambda s: mark_safe(LegalText.current_version(s).checkboxtextversion_set[0].get_content()),
    #     lambda s, v: v
    # )

    def __init__(self, slug=None, to=LegalTextVersion, **kwargs):
        self.slug = slug
        error_messages = {
            'incomplete': 'This field is required',
        }
        text = LegalText.current_version(slug)
        checkboxes = text.checkboxtextversion_set.all()
        fields_list = [forms.BooleanField(label='bla') for checkbox in checkboxes]
        fields = tuple(fields_list)
        labels = [checkbox.get_content() for checkbox in checkboxes]
        self.widget = MultipleCheckboxWidget(checkboxes)
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=True, label='bla bla bla', **kwargs)

    def compress(self, data_list):
        pass


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

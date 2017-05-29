try:
    import django
    django_version = django.__version__.split('.')
    assert int(django_version[0]) > 1 or int(django_version[1]) > 10
    from django import forms
except AssertionError:
    import floppyforms.__future__ as forms

from django.template import loader

from .models import LegalText


class CheckboxWidget(forms.widgets.MultiWidget):
    template_name = 'legaltext/checkboxwidget_django11.html'  # Django>=1.11

    def __init__(self, slug, attrs=None):
        self.version = LegalText.current_version(slug)
        self.checkboxes = self.version.checkboxtextversion_set.all()
        widgets = [forms.CheckboxInput() for checkbox in self.checkboxes]
        super(CheckboxWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        for checkbox_counter in range(len(self.checkboxes)):
            chackbox_name = '{}_{}'.format(name, checkbox_counter)
            if data.get(chackbox_name, None) is None:
                return None
        return self.version.pk

    def decompress(self, value):
        # Overwrite initial value from LegalTextField.
        # Checkboxes are by default empty.
        return [None for checkbox in self.checkboxes]

    def get_context(self, name, value, attrs=None):
        # This works for django >= 1.11.
        # It works together with template_name.
        context = super(CheckboxWidget, self).get_context(name, value, attrs)
        widgets = context['widget']['subwidgets']
        labels = [checkbox.get_content() for checkbox in self.checkboxes]
        context['widget']['subwidgets_checkboxes'] = zip(widgets, labels)
        return context

    def format_output(self, rendered_widgets):
        # This works for django < 1.11.
        return loader.render_to_string('legaltext/checkboxwidget_django19.html', {
            'widgets': [
                (widget, '{0}_{1}'.format(
                    self.context_instance['field'].name, i), checkbox.get_content())
                for i, widget, checkbox
                in zip(range(0, len(self.checkboxes)), rendered_widgets, self.checkboxes)
            ],
            'required': self.is_required,
            'errors': self.context_instance['field'].errors
        })

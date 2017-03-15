try:
    import floppyforms.__future__ as forms
except ImportError:
    from django import forms
from django.utils.safestring import mark_safe

from .models import LegalText


class CheckboxWidget(forms.widgets.MultiWidget):

    def __init__(self, slug, attrs=None):
        self.checkboxes = LegalText.current_version(slug).checkboxtextversion_set.all()
        self.version = LegalText.current_version(slug)
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
        # Checkboxes are bydefault empty.
        return [None for checkbox in self.checkboxes]

    def format_output(self, rendered_widgets):
        # This will work until django 1.10.
        # In django 1.11 format_output is removed
        # https://docs.djangoproject.com/en/dev/releases/1.11/
        result = ''
        for x, y in zip(rendered_widgets, self.checkboxes):
            result += u'<p class="placewidget">{} {}</p>'.format(x, y.get_content())
        return mark_safe(result)

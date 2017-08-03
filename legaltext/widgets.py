import floppyforms.__future__ as forms
from django.conf import settings
from django.template.loader import render_to_string

from .models import LegalText


class LegalTextWidget(forms.widgets.MultiWidget):
    template_name = None

    def __init__(self, slug, attrs=None):
        self.version = LegalText.current_version(slug)
        self.checkboxes = self.version.checkboxes.all()

        super(LegalTextWidget, self).__init__(
            [forms.CheckboxInput() for checkbox in self.checkboxes], attrs)

    def get_template_name(self):
        if self.template_name:
            return self.template_name

        template_name = getattr(
            settings, 'LEGALTEXT_WIDGET_TEMPLATE', 'legaltext/widget.html')
        overrides = getattr(settings, 'LEGALTEXT_WIDGET_TEMPLATE_OVERRIDES', {})
        return overrides.get(self.version.legaltext.slug, template_name)

    def value_from_datadict(self, data, files, name):
        for i, checkbox in enumerate(self.checkboxes):
            if not data.get('{}_{}'.format(name, i)):
                return None
        return self.version.pk

    def decompress(self, value):
        # Overwrite initial value from LegalTextField.
        # Checkboxes are by default empty.
        return [None for checkbox in self.checkboxes]

    def format_output(self, rendered_widgets):
        base_name = self.context_instance['field'].name
        return render_to_string(self.get_template_name(), {
            'required': self.is_required,
            'errors': self.context_instance['field'].errors,
            'version': self.version,
            'checkboxes': [(
                '{0}_{1}'.format(base_name, i),
                widget,
                checkbox.render_content()
            ) for i, widget, checkbox in zip(
                range(len(rendered_widgets)),
                rendered_widgets,
                self.checkboxes
            )]
        })

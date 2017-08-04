import floppyforms.__future__ as forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.text import mark_safe

from .models import LegalText


class LegalTextWidget(forms.widgets.MultiWidget):
    template_name = None

    def __init__(self, slug, attrs=None):
        self.version = LegalText.current_version(slug)
        self.checkboxes = list(self.version.checkboxes.all())

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

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        if not isinstance(value, list):
            value = self.decompress(value)

        final_attrs = self.build_attrs(attrs or {})
        final_attrs.update(getattr(settings, 'LEGALTEXT_WIDGET_ATTRS', {}))
        id_ = final_attrs.get('id')

        checkboxes = []
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None

            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))

            checkboxes.append((
                '{0}_{1}'.format(name, i),
                widget.render(name + '_%s' % i, widget_value, final_attrs),
                self.checkboxes[i].render_content()
            ))

        return mark_safe(render_to_string(self.get_template_name(), {
            'required': self.is_required,
            'errors': getattr(getattr(
                self, 'context_instance', {}).get('field'), 'errors', []),
            'version': self.version,
            'checkboxes': checkboxes
        }))

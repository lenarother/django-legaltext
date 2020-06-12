from unittest import mock

import floppyforms.__future__ as forms
import pytest

from legaltext.models import LegalTextVersion
from legaltext.widgets import LegalTextWidget
from testing.factories import LegalTextCheckboxFactory, LegalTextVersionFactory


@pytest.mark.django_db
class TestLegalTextWidget:

    def setup(self):
        self.legal_text_version = LegalTextVersionFactory.create(content='foo')
        self.checkbox1 = LegalTextCheckboxFactory.create(
            legaltext_version=self.legal_text_version, content='cb1')
        self.checkbox2 = LegalTextCheckboxFactory.create(
            legaltext_version=self.legal_text_version, content='cb2')

    def test_init(self):
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        assert isinstance(widget.version, LegalTextVersion)
        assert len(widget.checkboxes) == 2

        assert len(widget.widgets) == 2
        assert isinstance(widget.widgets[0], forms.CheckboxInput)

    def test_get_template_name_attribute(self):
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        widget.template_name = 'foo.html'
        assert widget.get_template_name() == 'foo.html'

    def test_get_template_name_default(self):
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        assert widget.get_template_name() == 'legaltext/widget.html'

    def test_get_template_name_custom(self, settings):
        settings.LEGALTEXT_WIDGET_TEMPLATE = 'bar.html'
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        assert widget.get_template_name() == 'bar.html'

    def test_get_template_name_override(self, settings):
        settings.LEGALTEXT_WIDGET_TEMPLATE_OVERRIDES = {'bar': 'baz.html'}
        widget = LegalTextWidget('foo')
        assert widget.get_template_name() == 'legaltext/widget.html'
        widget = LegalTextWidget('bar')
        assert widget.get_template_name() == 'baz.html'

    def test_value_from_datadict(self):
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        assert widget.value_from_datadict({}, {}, 'field') is None
        assert widget.value_from_datadict({'field_1': 1}, {}, 'field') is None
        assert widget.value_from_datadict(
            {'field_0': 1, 'field_1': 1}, {}, 'field') == widget.version.pk

    def test_decompress(self):
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        assert widget.decompress(None) == [None, None]
        assert widget.decompress(1) == [None, None]

    @mock.patch('legaltext.widgets.render_to_string')
    def test_render(self, render_mock):
        render_mock.return_value = 'rendered widget'
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        field = mock.Mock()
        field.name = 'field'
        field.errors = [1]
        widget.context_instance = {'field': field}
        widget.render('field', None)
        assert render_mock.called is True
        assert render_mock.call_args[0][0] == 'legaltext/widget.html'
        assert render_mock.call_args[0][1] == {
            'version': widget.version,
            'checkboxes': [
                ('field_0', '<input type="checkbox" name="field_0">\n', 'cb1'),
                ('field_1', '<input type="checkbox" name="field_1">\n', 'cb2')],
            'required': False,
            'errors': [1]
        }

    @mock.patch('legaltext.widgets.render_to_string')
    def test_render_extra_attrs(self, render_mock, settings):
        settings.LEGALTEXT_WIDGET_ATTRS = {'class': 'field'}
        render_mock.return_value = 'rendered widget'
        widget = LegalTextWidget(self.legal_text_version.legaltext.slug)
        widget.render('field', None)
        assert 'class="field"' in render_mock.call_args[0][1]['checkboxes'][0][1]

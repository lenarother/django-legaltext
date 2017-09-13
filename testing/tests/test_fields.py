import pytest
from django import forms
from django.db.models.fields import NOT_PROVIDED

from legaltext.fields import CurrentLegalText, LegalTextField, LegalTextFormField
from legaltext.models import LegalTextVersion
from legaltext.widgets import LegalTextWidget


@pytest.mark.django_db
class TestCurrentLegalText:

    def test_init(self):
        obj = CurrentLegalText('foo')
        assert obj.slug == 'foo'

    def test_call(self):
        obj = CurrentLegalText('foo')
        version_id = obj()
        version = LegalTextVersion.objects.get(pk=version_id)
        assert version.legaltext.slug == 'foo'


@pytest.mark.django_db
class TestLegalTextField:

    def test_init_with_slug(self):
        field = LegalTextField('foo')
        assert field.slug == 'foo'
        assert isinstance(field.default, CurrentLegalText)
        assert field.get_limit_choices_to() == {'legaltext__slug': 'foo'}
        assert field.remote_field.related_name == '+'
        assert field.blank is True
        assert field.null is True

    def test_init_without_slug(self):
        field = LegalTextField()
        assert field.slug is None
        assert field.default == NOT_PROVIDED
        assert field.get_limit_choices_to() == {}
        assert field.remote_field.related_name == '+'
        assert field.blank is True
        assert field.null is True

    def test_deconstruct(self):
        field = LegalTextField('foo')
        assert field.deconstruct()[3]['slug'] == 'foo'


@pytest.mark.django_db
class TestLegalTextFormField:

    def test_init_without_kwargs(self):
        field = LegalTextFormField('foo')
        assert field.slug == 'foo'
        assert isinstance(field.widget, LegalTextWidget)
        assert field.widget.version.legaltext.slug == 'foo'
        assert field.required is True

    def test_init_with_kwargs(self):
        field = LegalTextFormField('foo', required=False, widget=forms.HiddenInput)
        assert field.slug == 'foo'
        assert isinstance(field.widget, forms.HiddenInput)
        assert field.required is False

    def test_label(self):
        field = LegalTextFormField('foo')
        assert field.label == 'foo'
        field.label = 'bar'
        assert field.label == 'foo'

    def test_prepare_value(self):
        field = LegalTextFormField('foo')
        assert field.prepare_value(None) is False
        assert field.prepare_value(0) is False
        assert field.prepare_value(1) is True

    def test_to_python(self):
        field = LegalTextFormField('foo')
        assert field.to_python(None) is None
        assert field.to_python(0) is None
        assert isinstance(field.to_python(1), LegalTextVersion)
        assert isinstance(field.to_python(True), LegalTextVersion)

import pytest

from legaltext.tests.factories.legaltext import (
    CheckboxTextVersionFactory, LegalTextFactory, LegalTextVersionFactory)


@pytest.mark.django_db
class TestLegalText:

    def test_str(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text')

        assert str(legal_text) == 'Foo Bar Text'


@pytest.mark.django_db
class TestLegalTextVersion:

    def test_str(self):
        legal_text_version = LegalTextVersionFactory.create(legaltext__name='Foo Bar Text')

        assert 'Foo Bar Text' in str(legal_text_version)


@pytest.mark.django_db
class TestCheckboxTextVersion:

    def test_str(self):
        checkbox_text_version = CheckboxTextVersionFactory.create(
            legaltext_version__legaltext__name='Foo Bar Text')

        assert 'Foo Bar Text' in str(checkbox_text_version)
        assert 'Checkbox' in str(checkbox_text_version)

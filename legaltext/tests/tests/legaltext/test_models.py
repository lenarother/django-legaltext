from datetime import datetime
import pytest
from freezegun import freeze_time

from legaltext.models import LegalText, LegalTextVersion

from legaltext.tests.factories.legaltext import (
    CheckboxTextVersionFactory, LegalTextFactory, LegalTextVersionFactory)


@pytest.mark.django_db
class TestLegalText:

    def test_str(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text')

        assert str(legal_text) == 'Foo Bar Text'

    def test_current_version_no_version_yet(self):
        version = LegalText.current_version('test-version')

        assert isinstance(version, LegalTextVersion)
        assert version.legaltext.slug == 'test-version'
        assert version.legaltext.name == 'test-version'
        assert version.content == ''

    @freeze_time('2016-01-02')
    def test_current_version(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text', slug='foo-bar')

        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=datetime(2015, 1, 1, 10, 0))
        version_present = LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=datetime(2016, 1, 1, 10, 0))
        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=datetime(2017, 1, 1, 10, 0))

        version = LegalText.current_version('foo-bar')

        assert version.legaltext.slug == 'foo-bar'
        assert version.legaltext.name == 'Foo Bar Text'
        assert version.pk == version_present.pk

    def test_get_current_version_no_version_yet(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text')
        version = legal_text.get_current_version()

        assert version.legaltext.slug == 'foo-bar-text'
        assert version.legaltext.name == 'Foo Bar Text'
        assert version.content == ''

    @freeze_time('2016-01-02')
    def test_get_current_version(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text', slug='foo-bar-test')

        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=datetime(2015, 1, 1, 10, 0),
            content='Test content 1')
        version_present = LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=datetime(2016, 1, 1, 10, 0),
            content='Test content 2')
        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=datetime(2017, 1, 1, 10, 0),
            content='Test content 3')

        version = legal_text.get_current_version()

        assert version.legaltext.slug == 'foo-bar-test'
        assert version.legaltext.name == 'Foo Bar Text'
        assert version.content == 'Test content 2'
        assert version.pk == version_present.pk


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

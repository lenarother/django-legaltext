from datetime import datetime
import pytest
import pytz
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
        utc = pytz.utc

        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=utc.localize(datetime(2015, 1, 1, 10, 0)))
        version_present = LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=utc.localize(datetime(2016, 1, 1, 10, 0)))
        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=utc.localize(datetime(2017, 1, 1, 10, 0)))

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
        utc = pytz.utc

        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=utc.localize(datetime(2015, 1, 1, 10, 0)),
            content='Test content 1')
        version_present = LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=utc.localize(datetime(2016, 1, 1, 10, 0)),
            content='Test content 2')
        LegalTextVersionFactory.create(
            legaltext=legal_text, valid_from=utc.localize(datetime(2017, 1, 1, 10, 0)),
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

    def test_get_content(self):
        legal_text_version = LegalTextVersionFactory.create(content='Text Text Text')

        assert legal_text_version.get_content() == 'Text Text Text'

    def test_get_content_with_anchor(self):
        legal_text_version = LegalTextVersionFactory.create(
            content='Text [[foo]]Text[[end]] Text')

        assert legal_text_version.get_content() == (
            'Text <div class="foo"><span class="anchor" id="foo"></span>Text</div> Text')


@pytest.mark.django_db
class TestCheckboxTextVersion:

    def test_str(self):
        checkbox = CheckboxTextVersionFactory.create(
            legaltext_version__legaltext__name='Foo Bar Text')

        assert 'Foo Bar Text' in str(checkbox)
        assert 'Checkbox' in str(checkbox)

    def test_slug(self):
        checkbox = CheckboxTextVersionFactory.create(
            legaltext_version__legaltext__slug='foo-bar-text')

        assert checkbox.slug == 'foo-bar-text'

    def test_get_content(self):
        checkbox = CheckboxTextVersionFactory.create(content='Checkbox test text', )

        assert checkbox.get_content() == 'Checkbox test text'

    def test_get_content_with_link(self):
        checkbox = CheckboxTextVersionFactory.create(
            content='Checkbox [[test]] text', anchor='',
            legaltext_version__legaltext__slug='test-1')

        assert checkbox.get_content() == (
            'Checkbox <a href="/test-1" title="test">test</a> text')

    def test_get_content_with_link_and_anchor(self):
        checkbox = CheckboxTextVersionFactory.create(
            content='Checkbox [[test]] text', anchor='important',
            legaltext_version__legaltext__slug='test-2')

        assert checkbox.get_content() == (
            'Checkbox <a href="/test-2#important" title="test">test</a> text')

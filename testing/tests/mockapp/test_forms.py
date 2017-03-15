import pytest

from examples.mockapp.constants import MOCKAPP_PRIVACY_SLUG, MOCKAPP_TERMS_SLUG
from examples.mockapp.forms import MockappParticipationForm
from examples.mockapp.models import MockSurveyParticipant
from testing.factories.legaltext import (CheckboxTextVersionFactory,
                                         LegalTextFactory,
                                         LegalTextVersionFactory)


@pytest.mark.django_db
class TestParticipantForm:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.terms = LegalTextFactory(slug=MOCKAPP_TERMS_SLUG)
        self.privacy = LegalTextFactory(slug=MOCKAPP_PRIVACY_SLUG)
        self.terms_version = LegalTextVersionFactory(legaltext=self.terms)
        self.privacy_version = LegalTextVersionFactory(legaltext=self.privacy)
        CheckboxTextVersionFactory(
            legaltext_version=self.terms_version, content='Terms Checkbox 1')
        CheckboxTextVersionFactory(
            legaltext_version=self.privacy_version, content='Privacy Checkbox 1')
        CheckboxTextVersionFactory(
            legaltext_version=self.privacy_version, content='Privacy Checkbox 2')
        CheckboxTextVersionFactory(
            legaltext_version=self.privacy_version, content='Privacy Checkbox 3')

        self.form_data = {
            'name': 'Test Name',
            'accepted_terms_0': True,
            'accepted_privacy_0': True,
            'accepted_privacy_1': True,
            'accepted_privacy_2': True,
        }

    def test_form_valid(self):
        form = MockappParticipationForm(self.form_data)

        assert form.is_valid() is True

    def test_form_invalid(self):
        form = MockappParticipationForm({})

        assert form.is_valid() is False
        assert len(form.errors) == 3

    def test_terms(self):
        form = MockappParticipationForm(self.form_data)
        form.save()
        participant = MockSurveyParticipant.objects.first()

        assert MockSurveyParticipant.objects.count() == 1
        assert participant.accepted_terms == self.terms_version

    def test_privacy(self):
        form = MockappParticipationForm(self.form_data)
        form.save()
        participant = MockSurveyParticipant.objects.first()

        assert MockSurveyParticipant.objects.count() == 1
        assert participant.accepted_privacy == self.privacy_version

    def test_form_rendering(self):
        form = MockappParticipationForm()
        form_html = form.as_p()

        for checkbox in self.terms_version.checkboxtextversion_set.all():
            assert checkbox.get_content() in form_html

        for checkbox in self.privacy_version.checkboxtextversion_set.all():
            assert checkbox.get_content() in form_html

    def test_form_checkboxes_are_empty_bydefault(self):
        form = MockappParticipationForm()
        form_html = form.as_p()

        assert 'checked="checked"' not in form_html


@pytest.mark.django_db
class TestParticipantFormNoLegaltextData:

    def test_form_valid(self):
        form = MockappParticipationForm({'name': 'Foo'})

        assert form.is_valid() is True

    def test_form_invalid(self):
        form = MockappParticipationForm({})

        assert form.is_valid() is False
        assert len(form.errors) == 1

    def test_form_rendering(self):
        form = MockappParticipationForm()
        form_html = form.as_table()

        assert form_html.count('<tr>') == 1
        assert 'checkbox' not in form_html

    def test_terms(self):
        form = MockappParticipationForm({'name': 'Foo'})
        form.save()
        participant = MockSurveyParticipant.objects.first()

        assert MockSurveyParticipant.objects.count() == 1
        assert participant.accepted_terms.legaltext.slug == MOCKAPP_TERMS_SLUG
        assert participant.accepted_terms.get_content() == ''

    def test_privacy(self):
        form = MockappParticipationForm({'name': 'Foo'})
        form.save()
        participant = MockSurveyParticipant.objects.first()

        assert MockSurveyParticipant.objects.count() == 1
        assert participant.accepted_privacy.legaltext.slug == MOCKAPP_PRIVACY_SLUG
        assert participant.accepted_privacy.get_content() == ''

from django.forms import ModelForm

from legaltext.fields import (CheckboxWidget, LegalTextCheckboxFormField,
                              MultiCheckboxFormField, add_legaltext_checkboxes)
from legaltext.models import LegalText

from .constants import MOCKAPP_PRIVACY_SLUG, MOCKAPP_TERMS_SLUG
from .models import MockSurveyParticipant


class MockappParticipationForm(ModelForm):

    class Meta:
        model = MockSurveyParticipant
        exclude = ()
        fields = (
            'name',
            'accepted_privacy',
            'accepted_terms',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # # add single checkbox with known field name
        # legaltext_version = LegalText.current_version(MOCKAPP_TERMS_SLUG)
        # terms_checkbox = legaltext_version.checkboxtextversion_set.first()
        # self.fields['accepted_terms'] = LegalTextCheckboxFormField(terms_checkbox)

        # # add all fields automatically
        # add_legaltext_checkboxes(self.fields, MOCKAPP_PRIVACY_SLUG)
        # self.fields['privacy'] = MultiCheckboxFormField(MOCKAPP_PRIVACY_SLUG)
        self.fields['accepted_privacy'].widget = CheckboxWidget(MOCKAPP_PRIVACY_SLUG)
        self.fields['accepted_terms'].widget = CheckboxWidget(MOCKAPP_TERMS_SLUG)
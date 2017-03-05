from django.forms import ModelForm

from legaltext.fields import (LegalTextCheckboxFormField,
                              add_legaltext_checkboxes, CheckboxFormField)
from legaltext.models import LegalText

from .constants import MOCKAPP_PRIVACY_SLUG, MOCKAPP_TERMS_SLUG
from .models import MockSurveyParticipant


class MockappParticipationForm(ModelForm):

    class Meta:
        model = MockSurveyParticipant
        fields = (
            'name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add single checkbox with known field name
        legaltext_version = LegalText.current_version(MOCKAPP_TERMS_SLUG)
        terms_checkbox = legaltext_version.checkboxtextversion_set.first()
        self.fields['accepted_terms'] = LegalTextCheckboxFormField(terms_checkbox)

        # add all fields automatically
        # add_legaltext_checkboxes(self.fields, MOCKAPP_PRIVACY_SLUG)
        self.fields['privasy'] = CheckboxFormField(MOCKAPP_PRIVACY_SLUG)

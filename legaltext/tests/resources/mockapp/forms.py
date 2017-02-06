from django.forms import ModelForm

from legaltext.fields import add_legaltext_checkboxes

from .constants import MOCKAPP_TERMS_SLUG, MOCKAPP_PRIVACY_SLUG
from .models import MockSurveyParticipant


class MockappParticipationForm(ModelForm):

    class Meta:
        model = MockSurveyParticipant
        fields = (
            'name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_legaltext_checkboxes(self.fields, MOCKAPP_TERMS_SLUG)
        add_legaltext_checkboxes(self.fields, MOCKAPP_PRIVACY_SLUG)

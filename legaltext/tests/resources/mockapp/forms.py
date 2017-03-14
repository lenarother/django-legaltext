from django.forms import ModelForm

from legaltext.widgets import CheckboxWidget

from .constants import MOCKAPP_PRIVACY_SLUG, MOCKAPP_TERMS_SLUG
from .models import MockSurveyParticipant


class MockappParticipationForm(ModelForm):

    class Meta:
        model = MockSurveyParticipant
        fields = ('name', 'accepted_privacy', 'accepted_terms')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accepted_privacy'].widget = CheckboxWidget(MOCKAPP_PRIVACY_SLUG)
        self.fields['accepted_privacy'].required = True
        self.fields['accepted_terms'].widget = CheckboxWidget(MOCKAPP_TERMS_SLUG)
        self.fields['accepted_terms'].required = True

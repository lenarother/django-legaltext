import floppyforms.__future__ as forms

from legaltext.fields import LegalTextFormField

from .constants import PRIVACY_SLUG, TERMS_SLUG
from .models import Participant


class ParticipationForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('date_submit',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accepted_privacy'] = LegalTextFormField(PRIVACY_SLUG)
        self.fields['accepted_terms'] = LegalTextFormField(TERMS_SLUG)

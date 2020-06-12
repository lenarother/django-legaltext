import floppyforms.__future__ as forms

from legaltext.fields import LegalTextFormField

from .models import Participant


class ParticipationForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('date_submit',)

    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        super().__init__(*args, **kwargs)
        self.fields['accepted_privacy'] = LegalTextFormField(self.survey.privacy.slug)
        self.fields['accepted_terms'] = LegalTextFormField(self.survey.terms.slug)

from legaltext.widgets import CheckboxWidget

from .constants import MOCKAPP_PRIVACY_SLUG, MOCKAPP_TERMS_SLUG
from .models import MockSurveyParticipant

try:
    import django
    django_version = django.__version__.split('.')
    assert int(django_version[0]) > 1 or int(django_version[1]) > 10
    from django import forms
except AssertionError:
    import floppyforms.__future__ as forms


class MockappParticipationForm(forms.ModelForm):

    class Meta:
        model = MockSurveyParticipant
        fields = ('name', 'accepted_privacy', 'accepted_terms')

    def __init__(self, *args, **kwargs):
        super(MockappParticipationForm, self).__init__(*args, **kwargs)
        self.fields['accepted_privacy'].widget = CheckboxWidget(MOCKAPP_PRIVACY_SLUG)
        self.fields['accepted_privacy'].required = True
        self.fields['accepted_terms'].widget = CheckboxWidget(MOCKAPP_TERMS_SLUG)
        self.fields['accepted_terms'].required = True

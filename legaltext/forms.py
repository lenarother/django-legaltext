from django import forms

from .models import LegalTextVersion


class LegalTextVersionAdminForm(forms.ModelForm):

    class Meta:
        model = LegalTextVersion
        exclude = ()

    def __init__(self, *args, **kwargs):
        legaltext_pk = kwargs.get('initial', {}).get('legaltext')
        if legaltext_pk:
            previous_text = LegalTextVersion.objects.filter(
                legaltext=legaltext_pk).first()
            if previous_text:
                kwargs['initial']['content'] = previous_text.content

        super(LegalTextVersionAdminForm, self).__init__(*args, **kwargs)

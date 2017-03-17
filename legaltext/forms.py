try:
    import floppyforms.__future__ as forms
except ImportError:
    from django import forms
from .models import LegalTextVersion


class LegalTextVersionAdminForm(forms.ModelForm):

    class Meta:
        model = LegalTextVersion
        exclude = []

    def __init__(self, *args, **kwargs):
        legaltext_pk = kwargs.get('initial', {}).get('legaltext')
        if legaltext_pk:
            previous_text = LegalTextVersion.objects.filter(
                legaltext=legaltext_pk).first().content
            kwargs['initial'].update({'content': previous_text})
        super().__init__(*args, **kwargs)

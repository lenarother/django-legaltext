from django import forms
from django.forms.models import BaseInlineFormSet, ModelForm

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


class CustomInlineFormset(BaseInlineFormSet):
    """
    Custom formset that support initial data
    Implementation based on:
    http://www.catharinegeek.com/how-to-set-initial-data-for-inline-model-formset-in-django/
    """

    def initial_form_count(self):
        """
        set 0 to use initial_extra explicitly.
        """
        if self.initial_extra:
            return 0
        else:
            return BaseInlineFormSet.initial_form_count(self)

    def total_form_count(self):
        """
        here use the initial_extra len to determine needed forms
        """
        if self.initial_extra:
            count = len(self.initial_extra) if self.initial_extra else 0
            count += self.extra
            return count
        else:
            return BaseInlineFormSet.total_form_count(self)


class CustomModelForm(ModelForm):
    """
    Custom model form that support initial data when save.
    Implementation based on:
    http://www.catharinegeek.com/how-to-set-initial-data-for-inline-model-formset-in-django/
    """

    def has_changed(self):
        """
        Returns True if we have initial data.
        """
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)

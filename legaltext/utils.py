"""
Helper for admin inlines that support initial data
Implementation based on:
http://www.catharinegeek.com/how-to-set-initial-data-for-inline-model-formset-in-django/
"""
from functools import partialmethod

from django.contrib import admin
from django.forms.models import BaseInlineFormSet, ModelForm


class InitialExtraInlineFormset(BaseInlineFormSet):

    def initial_form_count(self):
        if self.initial_extra:
            return 0
        else:
            return BaseInlineFormSet.initial_form_count(self)

    def total_form_count(self):
        if self.initial_extra:
            count = len(self.initial_extra) if self.initial_extra else 0
            count += self.extra
            return count
        else:
            return BaseInlineFormSet.total_form_count(self)


class InitialExtraModelForm(ModelForm):

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)


class InitialExtraStackedInline(admin.StackedInline):

    form = InitialExtraModelForm
    formset = InitialExtraInlineFormset

    def get_extra(self, *args, **kwargs):
        if 'initial' in kwargs:
            return len(kwargs['initial'])
        return super().get_extra(*args, **kwargs)

    def get_initial_extra(self, request, obj=None):
        return []

    def get_formset(self, request, obj=None, **kwargs):
        initial = self.get_initial_extra(request, obj)
        formset = super().get_formset(request, obj, **kwargs)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        return formset

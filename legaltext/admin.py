from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .actions import Exporter
from .models import LegalText, LegalTextCheckbox, LegalTextVersion
from .utils import InitialExtraStackedInline


class LegalTextVersionAdminForm(forms.ModelForm):

    class Meta:
        model = LegalTextVersion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        legaltext_id = (kwargs.get('initial') or {}).get('legaltext', None)
        if legaltext_id:
            current_version = LegalTextVersion.objects.filter(
                legaltext=legaltext_id).first()
            if current_version:
                kwargs.setdefault('initial', {})['content'] = current_version.content

        super().__init__(*args, **kwargs)


class LegalTextAdminForm(forms.ModelForm):

    class Meta:
        model = LegalText
        fields = '__all__'

    def clean_url_name(self):
        url_name = self.cleaned_data['url_name']
        if not url_name:
            return None
        return url_name


@admin.register(LegalText)
class LegalTextAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_version_link', 'add_new_version_link')
    search_fields = ('name',)
    form = LegalTextAdminForm

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)} if obj is None else {}

    def get_readonly_fields(self, request, obj=None):
        return ('slug',) if obj else ()

    def current_version_link(self, obj):
        version = obj.get_current_version()
        return '<a href="{0}">{1:%x %X}</a>'.format(
            reverse('admin:legaltext_legaltextversion_change', args=(version.pk,)),
            timezone.localtime(version.valid_from)
        )
    current_version_link.allow_tags = True
    current_version_link.short_description = _('Current version')

    def add_new_version_link(self, obj):
        return '<a href="{0}?legaltext={1}">{2}</a>'.format(
            reverse('admin:legaltext_legaltextversion_add'),
            obj.pk,
            gettext('Add new version')
        )
    add_new_version_link.allow_tags = True
    add_new_version_link.short_description = _('Add new version')


class LegalTextCheckboxInline(InitialExtraStackedInline):
    model = LegalTextCheckbox
    extra = 0
    min_num = 1

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.valid_from <= timezone.now():
            return ('content', 'order')
        return ()

    def get_max_num(self, request, obj=None):
        if obj and obj.valid_from <= timezone.now():
            return obj.checkboxes.count()
        return None

    def get_initial_extra(self, request, obj=None):
        initial = []
        if obj is None and request.method == 'GET' and 'legaltext' in request.GET:
            legaltext = LegalText.objects.filter(pk=request.GET['legaltext']).first()
            if legaltext:
                for checkbox in legaltext.get_current_version().checkboxes.all():
                    initial.append({'content': checkbox.content, 'order': checkbox.order})
        return initial


@admin.register(LegalTextVersion)
class LegalTextVersionAdmin(admin.ModelAdmin):
    list_display = ('legaltext_name', 'valid_from')
    list_filter = ('legaltext',)
    inlines = (LegalTextCheckboxInline,)
    form = LegalTextVersionAdminForm
    actions = (Exporter.export_legaltext_version_action(),)

    def get_fieldsets(self, request, obj=None):
        if obj is None or obj.valid_from > timezone.now():
            return super().get_fieldsets(request, obj)

        return ((None, {'fields': ('legaltext', 'valid_from', 'rendered_content')}),)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.valid_from <= timezone.now():
            return ('legaltext', 'valid_from', 'rendered_content')
        return ()

    def legaltext_name(self, obj):
        return obj.legaltext.name
    legaltext_name.short_description = _('Legal text')

    def rendered_content(self, obj):
        return obj.render_content()
    rendered_content.allow_tags = True
    rendered_content.short_description = _('Text')

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from markymark.utils import render_markdown

from .models import LegalText, LegalTextVersion


@admin.register(LegalText)
class LegalTextAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_version_link', 'add_new_version_link')
    search_fields = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)} if obj is None else {}

    def get_readonly_fields(self, request, obj=None):
        return ('slug',) if obj else ()

    def current_version_link(self, obj):
        version = obj.get_current_version()
        return u'<a href="{0}">{1:%x %X}</a>'.format(
            reverse('admin:legaltext_legaltextversion_change', args=(version.pk,)),
            timezone.localtime(version.valid_from)
        )
    current_version_link.allow_tags = True
    current_version_link.short_description = _('Current version')

    def add_new_version_link(self, obj):
        return u'<a href="{0}?legaltext={1}">{2}</a>'.format(
            reverse('admin:legaltext_legaltextversion_add'),
            obj.pk,
            ugettext('Add new version')
        )
    add_new_version_link.allow_tags = True
    add_new_version_link.short_description = _('Add new version')


@admin.register(LegalTextVersion)
class LegalTextVersionAdmin(admin.ModelAdmin):
    list_display = ('legaltext_name', 'valid_from')
    list_filter = ('legaltext',)

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj) if obj is None else (
            (None, {'fields': (
                'legaltext',
                'valid_from',
                'rendered_content',
                'rendered_checkbox_label'
            )}),
        )

    def get_readonly_fields(self, request, obj=None):
        return (
            'legaltext',
            'valid_from',
            'rendered_content',
            'rendered_checkbox_label'
        ) if obj else ()

    def legaltext_name(self, obj):
        return obj.legaltext.name
    legaltext_name.short_description = _('Legal text')

    def rendered_content(self, obj):
        return render_markdown(obj.content)
    rendered_content.allow_tags = True
    rendered_content.short_description = _('Text')

    def rendered_checkbox_label(self, obj):
        return obj.checkbox_label
    rendered_checkbox_label.allow_tags = True
    rendered_checkbox_label.short_description = _('Checkbox label')

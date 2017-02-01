from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import LegalText, LegalTextVersion


class LegalTextAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_version_link', 'add_new_version_link')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_prepopulated_fields(self, request, obj=None):
        prepopulated_fields = dict(
            **super(LegalTextAdmin, self).get_prepopulated_fields(request, obj))

        if obj is not None:
            del prepopulated_fields['slug']

        return prepopulated_fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(LegalTextAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ('slug',)
        return readonly_fields

    def current_version_link(self, obj):
        url = reverse(
            'admin:legaltext_legaltextversion_change', args=[obj.current_version.id])
        return u'<a href="%s">%s</a>' % (url, obj.current_version.valid_from_display)

    current_version_link.allow_tags = True
    current_version_link.short_description = _('Current version')

    def add_new_version_link(self, obj):
        url = reverse('admin:legaltext_legaltextversion_add')
        return u'<a href="%s?legaltext=%s">Add new version</a>' % (url, obj.pk)

    add_new_version_link.allow_tags = True
    add_new_version_link.short_description = _('Add new version')

admin.site.register(LegalText, LegalTextAdmin)


class LegalTextVersionAdmin(admin.ModelAdmin):
    list_display = ('legaltext', 'valid_from')
    list_filter = ('legaltext',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(LegalTextVersionAdmin, self).get_fieldsets(request, obj)
        if obj:
            fieldsets = ((None, {'fields': (
                'legaltext', 'valid_from', 'rendered_content', 'checkbox_text')}),)
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(LegalTextVersionAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + (
                'legaltext', 'valid_from', 'rendered_content', 'checkbox_text')
        return readonly_fields

    def rendered_content(self, obj):
        return obj.content

    rendered_content.allow_tags = True
    rendered_content.short_description = _('Text')

    class Media:
        js = (
            settings.FEINCMS_RICHTEXT_INIT_CONTEXT['TINYMCE_JS_URL'],
            settings.FEINCMS_RICHTEXT_INIT_CONTEXT['TINYMCE_SETTINGS_URL'],
            settings.FEINCMS_RICHTEXT_INIT_CONTEXT['TINYMCE_INIT_URL'],
        )

admin.site.register(LegalTextVersion, LegalTextVersionAdmin)

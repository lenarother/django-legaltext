from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from markymark.utils import render_markdown

from .models import CheckboxTextVersion, LegalText, LegalTextVersion


class CheckboxTextVersionInline(admin.StackedInline):
    model = CheckboxTextVersion
    extra = 3

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if request.method == "GET":
            version = LegalText.objects.get(pk=request.GET['legaltext']).get_current_version()
            checkboxes = version.checkboxtextversion_set.all()

            for checkbox in checkboxes:
                initial.append({
                    'content': checkbox.content,
                    'anchor': checkbox.anchor
                })
            self.extra = len(initial) or 1
        formset = super(CheckboxTextVersionInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)

        return formset


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
    inlines = (CheckboxTextVersionInline,)

    def get_form(self, request, obj=None, **kwargs):
        previous_text = self.model.objects.filter(
            legaltext=request.GET['legaltext']).first().content
        form = super(LegalTextVersionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['content'].initial = previous_text
        return form

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj) if obj is None else (
            (None, {'fields': (
                'legaltext',
                'valid_from',
                'rendered_content',
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

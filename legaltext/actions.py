import io
import zipfile

from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _


def export_legal_text_version_action(description=None):

    def get_file_name(legaltext, checkbox_i=None):
        content_type = 'content'
        if checkbox_i:
            content_type = 'checkbox{0}'.format(checkbox_i)

        return '{dt}_{pk}_{slug}_{content_type}.md'.format(
            dt=localtime(legaltext.valid_from).strftime('%Y%m%d_%H%M%S'),
            pk=legaltext.pk,
            slug=legaltext.legaltext.slug,
            content_type=content_type,
        )

    def export_legal_text_version(modeladmin, request, queryset):
        buff = io.BytesIO()
        archive = zipfile.ZipFile(buff, 'w', zipfile.ZIP_DEFLATED)

        for legaltext in queryset:
            content = io.StringIO()
            content.write(legaltext.content)
            filename = get_file_name(legaltext)
            archive.writestr(filename, content.getvalue())

            # TODO: change i to checkbox.order when feature/sortable-checkbox is in master
            # TODO: and update translations
            for i, checkbox in enumerate(legaltext.checkboxes.all()):
                checkbox_content = io.StringIO()
                checkbox_content.write(checkbox.content)
                checkbox_filename = get_file_name(legaltext, i + 1)
                archive.writestr(checkbox_filename, checkbox_content.getvalue())

        dt_now = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
        zip_filename = 'legaltext_export_{0}.zip'.format(dt_now)
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'filename={0}'.format(zip_filename)

        archive.close()
        buff.flush()
        legaltext_zip = buff.getvalue()
        buff.close()

        response.write(legaltext_zip)
        return response

    export_legal_text_version.short_description = description or _(
        'Export selected texts as zip')
    return export_legal_text_version

import io
import zipfile

from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _


class Exporter(object):

    @staticmethod
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

    @staticmethod
    def get_archive_name():
        dt_now = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
        return 'legaltext_export_{0}.zip'.format(dt_now)

    @classmethod
    def write_files(cls, queryset):
        buff = io.BytesIO()
        archive = zipfile.ZipFile(buff, 'w', zipfile.ZIP_DEFLATED)

        for legaltext in queryset:
            filename = cls.get_file_name(legaltext)
            archive.writestr(filename, legaltext.content)

            for i, checkbox in enumerate(legaltext.checkboxes.all()):
                checkbox_filename = cls.get_file_name(legaltext, checkbox.order or (i + 1))
                archive.writestr(checkbox_filename, checkbox.content)

        archive.close()
        buff.flush()
        legaltext_zip = buff.getvalue()
        buff.close()
        return legaltext_zip

    @classmethod
    def export_legaltext_version(cls, modeladmin, request, queryset):
        legaltext_zip = cls.write_files(queryset)
        zip_name = cls.get_archive_name()
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'filename={0}'.format(zip_name)
        response.write(legaltext_zip)
        return response

    @classmethod
    def export_legaltext_version_action(cls, short_description=None):
        short_description = short_description or _('Export selected versions')
        setattr(cls.export_legaltext_version.__func__, 'short_description', short_description)
        return cls.export_legaltext_version

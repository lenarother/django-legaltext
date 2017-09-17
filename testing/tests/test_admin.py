from datetime import timedelta

import pytest
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from freezegun import freeze_time

from legaltext.admin import LegalTextAdmin, LegalTextCheckboxInline, LegalTextVersionAdmin
from legaltext.models import LegalText, LegalTextCheckbox, LegalTextVersion
from testing.factories import (
    LegalTextCheckboxFactory, LegalTextFactory, LegalTextVersionFactory)


@pytest.mark.django_db
class TestLegalTextAdmin:

    def setup(self):
        self.modeladmin = LegalTextAdmin(LegalText, admin.site)

    def test_prepopulated_fields(self, rf):
        assert 'slug' in self.modeladmin.get_prepopulated_fields(rf.get('/'), None)
        assert 'slug' not in self.modeladmin.get_prepopulated_fields(
            rf.get('/'), LegalTextFactory.create())

    def test_readonly_fields(self, rf):
        assert 'slug' not in self.modeladmin.get_readonly_fields(rf.get('/'), None)
        assert 'slug' in self.modeladmin.get_readonly_fields(
            rf.get('/'), LegalTextFactory.create())

    def test_current_version_link(self):
        legal_text = LegalTextFactory.create()
        html = self.modeladmin.current_version_link(legal_text)
        assert '/legaltextversion/{0}/change/'.format(
            legal_text.get_current_version().pk) in html

    def test_add_new_version_link(self):
        legal_text = LegalTextFactory.create()
        html = self.modeladmin.add_new_version_link(legal_text)
        assert '/legaltextversion/add/?legaltext={0}'.format(legal_text.pk) in html


@pytest.mark.django_db
class TestLegalTextCheckboxInline:

    def setup(self):
        self.modeladmin = LegalTextCheckboxInline(LegalTextCheckbox, admin.site)

    def test_readonly_fields(self, rf):
        assert 'content' not in self.modeladmin.get_readonly_fields(rf.get('/'), None)
        assert 'content' not in self.modeladmin.get_readonly_fields(
            rf.get('/'), LegalTextVersionFactory.create(
                valid_from=timezone.now() + timedelta(days=1)))
        assert 'content' in self.modeladmin.get_readonly_fields(
            rf.get('/'), LegalTextVersionFactory.create(valid_from=timezone.now()))

    def test_get_max_num(self, rf):
        assert self.modeladmin.get_max_num(rf.get('/'), None) is None
        assert self.modeladmin.get_max_num(rf.get('/'), LegalTextVersionFactory.create(
            valid_from=timezone.now() + timedelta(days=1))) is None
        assert self.modeladmin.get_max_num(rf.get('/'), LegalTextVersionFactory.create(
            valid_from=timezone.now())) == 0

    def test_get_initial_extra_add_not_found(self, rf):
        assert self.modeladmin.get_initial_extra(
            rf.get('/'), None) == []

        assert self.modeladmin.get_initial_extra(
            rf.get('/', data={'legaltext': 1}), None) == []

    def test_get_initial_extra_add(self, rf):
        cb = LegalTextCheckboxFactory.create(content='foo')
        assert self.modeladmin.get_initial_extra(
            rf.get('/', data={'legaltext': cb.legaltext_version.legaltext.pk}), None
        ) == [{'content': 'foo', 'order': cb.pk}]

    def test_get_initial_extra_change(self, rf):
        assert self.modeladmin.get_initial_extra(
            rf.get('/'), LegalTextVersionFactory.create()) == []


@pytest.mark.django_db
class TestLegalTextVersionAdmin:

    def setup(self):
        self.modeladmin = LegalTextVersionAdmin(LegalTextVersion, admin.site)

    def test_get_fieldsets(self, rf, admin_user):
        request = rf.get('/')
        request.user = admin_user
        assert self.modeladmin.get_fieldsets(
            request, None
        )[0][1]['fields'] == ['legaltext', 'valid_from', 'content']
        assert self.modeladmin.get_fieldsets(
            request, LegalTextVersionFactory.create(
                valid_from=timezone.now() + timedelta(days=1))
        )[0][1]['fields'] == ['legaltext', 'valid_from', 'content']
        assert self.modeladmin.get_fieldsets(
            request, LegalTextVersionFactory.create(valid_from=timezone.now())
        )[0][1]['fields'] == ('legaltext', 'valid_from', 'rendered_content')

    def test_readonly_fields(self, rf):
        assert self.modeladmin.get_readonly_fields(rf.get('/'), None) == ()
        assert self.modeladmin.get_readonly_fields(
            rf.get('/'), LegalTextVersionFactory.create(
                valid_from=timezone.now() + timedelta(days=1))) == ()
        assert self.modeladmin.get_readonly_fields(
            rf.get('/'), LegalTextVersionFactory.create(valid_from=timezone.now())
        ) == ('legaltext', 'valid_from', 'rendered_content')

    def test_legaltext_name(self):
        legal_text_version = LegalTextVersionFactory.create(legaltext__name='foo')
        assert self.modeladmin.legaltext_name(legal_text_version) == 'foo'

    def test_rendered_content(self):
        legal_text_version = LegalTextVersionFactory.create(content='foo')
        assert self.modeladmin.rendered_content(
            legal_text_version) == legal_text_version.render_content()

    def test_add_no_form_initial(self, rf, admin_user):
        request = rf.get('/')
        request.user = admin_user
        response = self.modeladmin.add_view(request)
        assert response.status_code == 200
        assert response.context_data['adminform'].form.initial == {}

    def test_add_invalid_form_initial(self, rf, admin_user):
        request = rf.get('/', data={'legaltext': 1})
        request.user = admin_user
        response = self.modeladmin.add_view(request)
        assert response.status_code == 200
        assert response.context_data['adminform'].form.initial == {'legaltext': '1'}

    def test_add_form_initial(self, rf, admin_user):
        legal_text_version = LegalTextVersionFactory.create(content='foobar')
        request = rf.get('/', data={'legaltext': legal_text_version.legaltext.pk})
        request.user = admin_user
        response = self.modeladmin.add_view(request)
        assert response.status_code == 200
        assert response.context_data['adminform'].form.initial == {
            'content': 'foobar', 'legaltext': '1'}

    @freeze_time('2016-01-02 09:21:55')
    def test_export_legaltext_version_action(self, admin_client):
        legal_text_version = LegalTextVersionFactory.create(content='foobar')
        url = reverse('admin:legaltext_legaltextversion_changelist')
        data = {
            'action': 'export_legaltext_version',
            '_selected_action': [str(legal_text_version.pk)]
        }
        response = admin_client.post(url, data)
        assert response['Content-Type'] == 'application/zip'
        assert response['Content-Disposition'] == (
            'filename=legaltext_export_2016-01-02_09-21-55.zip')

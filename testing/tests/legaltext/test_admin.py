import pytest
from django.core.urlresolvers import reverse

from testing.factories import (
    CheckboxTextVersionFactory, LegalTextFactory, LegalTextVersionFactory)


@pytest.mark.django_db
class TestLegalTextVersionAdmin():

    def test_current_version_content_as_default_for_new_version(self, admin_client):
        legaltext_content = 'Test legaltext content XXX-XXX-XXX'
        legal_text = LegalTextFactory.create(name='Foo Bar Text')
        LegalTextVersionFactory.create(legaltext=legal_text, content=legaltext_content)
        admin_url = '{0}?legaltext={1}'.format(
            reverse('admin:legaltext_legaltextversion_add'),
            legal_text.pk)
        response = admin_client.get(admin_url)

        assert legaltext_content in response.content.decode()

    def test_current_version_checkbox_content_as_default_for_new_version(self, admin_client):
        checkbox_text = 'Checkbox label test text'
        anchor_text = 'checkbox-foo-bar-anchor'
        legal_text = LegalTextFactory.create(name='Foo Bar Text')
        legaltext_version = LegalTextVersionFactory.create(legaltext=legal_text)
        CheckboxTextVersionFactory.create(
            legaltext_version=legaltext_version,
            content=checkbox_text,
            anchor=anchor_text
        )
        base_url = reverse('admin:legaltext_legaltextversion_add')
        url = '{0}?legaltext={1}'.format(base_url, legal_text.pk)
        response = admin_client.get(url)

        assert checkbox_text in response.content.decode()
        assert anchor_text in response.content.decode()

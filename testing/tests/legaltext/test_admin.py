import pytest
from django.core.urlresolvers import reverse

from testing.factories.legaltext import (LegalTextFactory,
                                         LegalTextVersionFactory)


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

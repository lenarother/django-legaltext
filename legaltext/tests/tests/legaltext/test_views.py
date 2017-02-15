import pytest
from django.core.urlresolvers import reverse

from legaltext.models import LegalTextVersion


@pytest.mark.django_db
class TestLegaltextView:

    def test_get(self, client):
        url = reverse('legaltext', kwargs={'slug': 'test-foo-bar'})
        response = client.get(url)

        assert response.status_code == 200
        assert isinstance(response.context['current_version'], LegalTextVersion)
        assert response.context['current_version'].legaltext.slug == 'test-foo-bar'

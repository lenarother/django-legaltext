import pytest
from django.core.urlresolvers import reverse

from legaltext.models import LegalTextVersion

from testing.factories import LegalTextFactory


@pytest.mark.django_db
class TestLegaltextView:

    def test_get(self, client):
        test_slug = 'test-foo-bar'
        LegalTextFactory.create(slug=test_slug)
        url = reverse('legaltext', kwargs={'slug': test_slug})
        response = client.get(url)

        assert response.status_code == 200
        assert isinstance(response.context['current_version'], LegalTextVersion)
        assert response.context['current_version'].legaltext.slug == test_slug

    def test_get_non_existing_legaltext(self, client):
        url = reverse('legaltext', kwargs={'slug': 'no-such-legaltext'})
        response = client.get(url)

        assert response.status_code == 404

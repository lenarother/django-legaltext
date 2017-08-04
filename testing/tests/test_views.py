import pytest
from django.core.urlresolvers import reverse

from legaltext.models import LegalTextVersion
from legaltext.views import LegaltextView
from testing.factories import LegalTextFactory


@pytest.mark.django_db
class TestLegaltextView:

    def test_get_template_names_default(self):
        view = LegaltextView()
        view.object = LegalTextFactory.create(slug='foo')
        assert view.get_template_names() == 'legaltext/content.html'

    def test_get_template_names_custom(self, settings):
        settings.LEGALTEXT_VIEW_TEMPLATE = 'bar.html'
        view = LegaltextView()
        view.object = LegalTextFactory.create(slug='foo')
        assert view.get_template_names() == 'bar.html'

    def test_get_template_names_override(self, settings):
        settings.LEGALTEXT_VIEW_TEMPLATE_OVERRIDES = {'bar': 'baz.html'}
        view = LegaltextView()
        view.object = LegalTextFactory.create(slug='foo')
        assert view.get_template_names() == 'legaltext/content.html'
        view = LegaltextView()
        view.object = LegalTextFactory.create(slug='bar')
        assert view.get_template_names() == 'baz.html'

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

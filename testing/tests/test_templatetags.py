import pytest
from django.core.urlresolvers import NoReverseMatch
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError

from testing.factories import LegalTextFactory


@pytest.mark.django_db
class TestLegaltextUrl:

    def test_slug(self):
        LegalTextFactory.create(slug='foo-bar-test')
        expected = '/foo-bar-test/'
        template = Template('{% load legaltext_tags %}{% legaltext_url "foo-bar-test" %}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == expected

    def test_slug_as_variable(self):
        LegalTextFactory.create(slug='foo-bar-test')
        expected = '/foo-bar-test/'
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "foo-bar-test" as my_url %}'
            '{{ my_url }}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == expected

    def test_slug_as_variable_not_rendered(self):
        LegalTextFactory.create(slug='foo-bar-test')
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "foo-bar-test" as my_url %}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == ''

    def test_url_name(self):
        LegalTextFactory.create(slug='foo-bar-test', url_name='eggs')
        expected = '/eggs/'
        template = Template('{% load legaltext_tags %}{% legaltext_url "eggs" %}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == expected

    def test_url_name_as_variable(self):
        LegalTextFactory.create(slug='foo-bar-test', url_name='eggs')
        expected = '/eggs/'
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "eggs" as my_url %}'
            '{{ my_url }}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == expected

    def test_url_name_as_variable_not_rendered(self):
        LegalTextFactory.create(slug='foo-bar-test', url_name='eggs')
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "eggs" as my_url %}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == ''

    def test_slug_and_url_name(self):
        LegalTextFactory.create(slug='foo-bar-test', url_name='eggs')
        expected = '/eggs/'
        template = Template('{% load legaltext_tags %}{% legaltext_url "foo-bar-test" %}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == expected

    def test_no_legaltext(self):
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "foo-bar-test" %}')
        context = Context({})

        with pytest.raises(NoReverseMatch):
            template.render(context)

    def test_no_legaltext_as_variable(self):
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "foo-bar-test" as my_url %}'
            '{{ my_url }}')
        context = Context({})

        with pytest.raises(NoReverseMatch):
            template.render(context)

    def test_no_legaltext_silent(self, settings):
        settings.LEGALTEXT_SILENCE_TEMPLATE_ERRORS = True
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "foo-bar-test" %}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == ''

    def test_no_legaltext_as_variable_silence(self, settings):
        settings.LEGALTEXT_SILENCE_TEMPLATE_ERRORS = True
        template = Template(
            '{% load legaltext_tags %}{% legaltext_url "foo-bar-test" as my_url %}'
            '{{ my_url }}')
        context = Context({})

        rendered = template.render(context)

        assert rendered == ''

    def test_no_args(self):
        with pytest.raises(TemplateSyntaxError):
            template = Template(
                '{% load legaltext_tags %}{% legaltext_url %}')
            context = Context({})

            template.render(context)

    def test_no_args_as_variable(self):
        with pytest.raises(TemplateSyntaxError):
            template = Template(
                '{% load legaltext_tags %}{% legaltext_url as foo %}')
            context = Context({})

            template.render(context)

    def test_to_many_args(self):
        with pytest.raises(TemplateSyntaxError):
            template = Template(
                '{% load legaltext_tags %}{% legaltext_url "Foo" "Bar" %}')
            context = Context({})

            template.render(context)

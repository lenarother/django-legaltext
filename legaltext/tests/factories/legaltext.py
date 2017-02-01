import factory
from django.utils.text import slugify
from django.utils import timezone

from legaltext.models import LegalText, LegalTextVersion


class LegalTextFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda i: 'Legal Text Test {0}'.format(i))
    slug = factory.LazyAttribute(lambda a: slugify((a.name)))

    class Meta:
        model = LegalText


class LegalTextVersionFactory(factory.DjangoModelFactory):

    legaltext = factory.SubFactory(LegalTextFactory)
    valid_from = timezone.now()
    checkbox_text = factory.Sequence(lambda m: 'Accept test terms {0}'.format(m))
    content = factory.Sequence(
        lambda j: 'Legal Text test text test text test text {0}'.format(j))

    class Meta:
        model = LegalTextVersion

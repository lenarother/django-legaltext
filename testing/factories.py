import factory
from django.utils import timezone
from django.utils.text import slugify

from legaltext.models import LegalText, LegalTextCheckbox, LegalTextVersion


class LegalTextFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda i: 'Legal Text Test {0}'.format(i))
    slug = factory.LazyAttribute(lambda a: slugify((a.name)))

    class Meta:
        model = LegalText


class LegalTextVersionFactory(factory.DjangoModelFactory):
    legaltext = factory.SubFactory(LegalTextFactory)
    valid_from = timezone.now()
    content = factory.Sequence(lambda j: 'Legal Text test text test text {0}'.format(j))

    class Meta:
        model = LegalTextVersion


class LegalTextCheckboxFactory(factory.DjangoModelFactory):
    legaltext_version = factory.SubFactory(LegalTextVersionFactory)
    content = factory.Sequence(lambda k: 'Checkbox Label Test Text {0}'.format(k))

    class Meta:
        model = LegalTextCheckbox

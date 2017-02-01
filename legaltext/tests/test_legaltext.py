import pytest

from legaltext.tests.factories.legaltext import LegalTextFactory


@pytest.mark.django_db
class TestLegalText:

    def test_str(self):
        legal_text = LegalTextFactory.create(name='Foo Bar Text')

        assert str(legal_text) == 'Foo Bar Text'

    def test_current(self):
        legal_text = LegalTextFactory.create()
        # import pdb; pdb.set_trace()

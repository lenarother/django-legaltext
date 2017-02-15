import pytest
from django.db import connection

from legaltext.fields import LegalTextField
from legaltext.models import LegalTextVersion


@pytest.mark.django_db
class TestLegaltextField():

    def test_db_parameters_respects_db_type(self):
        legal_field = LegalTextField()
        assert legal_field.db_parameters(connection)['type'] == 'integer'

    def test_default(self):
        legal_field = LegalTextField('test-test-test')
        default = legal_field.default()

        assert isinstance(default, LegalTextVersion)
        assert default.legaltext.slug == legal_field.slug == 'test-test-test'

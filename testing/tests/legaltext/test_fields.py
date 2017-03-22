import pytest
from django.db import connection

from legaltext.fields import LegalTextField


@pytest.mark.django_db
class TestLegaltextField():

    def test_db_parameters_respects_db_type(self):
        legal_field = LegalTextField()
        assert legal_field.db_parameters(connection)['type'] == 'integer'

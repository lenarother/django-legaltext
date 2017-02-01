from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from legaltext.fields import LegalTextField


class MockSurveyParticipant(models.Model):
    name = models.CharField(max_length=255)

    accepted_terms = LegalTextField('my-survey-terms')
    accepted_privacy = LegalTextField('my-survay-privacy')
    date_submit = models.DateTimeField(_('Survey submission date'), default=timezone.now)

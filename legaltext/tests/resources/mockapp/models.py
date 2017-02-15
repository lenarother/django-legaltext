from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from legaltext.fields import LegalTextField

from .constants import MOCKAPP_PRIVACY_SLUG, MOCKAPP_TERMS_SLUG


class MockSurveyParticipant(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    accepted_terms = LegalTextField(MOCKAPP_TERMS_SLUG)
    accepted_privacy = LegalTextField(MOCKAPP_PRIVACY_SLUG)
    date_submit = models.DateTimeField(_('Survey submited date'), default=timezone.now)

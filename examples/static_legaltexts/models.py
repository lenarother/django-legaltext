from django.db import models
from django.utils import timezone

from legaltext.fields import LegalTextField

from .constants import PRIVACY_SLUG, TERMS_SLUG


class Participant(models.Model):
    name = models.CharField(max_length=255)

    accepted_terms = LegalTextField(TERMS_SLUG)
    accepted_privacy = LegalTextField(PRIVACY_SLUG)

    date_submit = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.date_submit)

from django.db import models
from django.urls import reverse
from django.utils import timezone

from legaltext.fields import LegalTextField
from legaltext.models import LegalText


class Survey(models.Model):
    name = models.CharField(max_length=255)
    terms = models.ForeignKey(LegalText, related_name='+', on_delete=models.CASCADE)
    privacy = models.ForeignKey(LegalText, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dynamic-form', args=(self.pk,))


class Participant(models.Model):
    name = models.CharField(max_length=255)

    accepted_terms = LegalTextField()
    accepted_privacy = LegalTextField()

    date_submit = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.date_submit)

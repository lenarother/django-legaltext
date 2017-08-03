from django.contrib import admin

from .models import Participant, Survey


admin.site.register(Participant)
admin.site.register(Survey)

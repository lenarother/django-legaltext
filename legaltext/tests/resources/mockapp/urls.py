from django.conf.urls import include, url
from django.contrib import admin

import legaltext

from .views import MockappParticipantCompletedView, MockappParticipantFormView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^legaltext/', include('legaltext.urls')),

    url(r'^$', MockappParticipantFormView.as_view(), name='form'),
    url(r'^completed/$', MockappParticipantCompletedView.as_view(), name='form-completed'),
]

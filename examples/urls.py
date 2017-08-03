from django.conf.urls import include, url
from django.contrib import admin

from examples.dynamic_legaltexts.views import (
    DynamicParticipantCompletedView, DynamicParticipantFormView)
from examples.static_legaltexts.views import (
    StaticParticipantCompletedView, StaticParticipantFormView)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^legaltext/', include('legaltext.urls')),

    url(
        r'^static-legaltext/$',
        StaticParticipantFormView.as_view(),
        name='static-form'),
    url(
        r'^static-legaltext/completed/$',
        StaticParticipantCompletedView.as_view(),
        name='static-form-completed'
    ),
    url(
        r'^dynamic-legaltext/(?P<id>\d+)/$',
        DynamicParticipantFormView.as_view(),
        name='dynamic-form'),
    url(
        r'^dynamic-legaltext/completed/$',
        DynamicParticipantCompletedView.as_view(),
        name='dynamic-form-completed'),
]

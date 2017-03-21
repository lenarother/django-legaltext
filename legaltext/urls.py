from django.conf.urls import url

from .views import LegaltextView


urlpatterns = [
    url(r'^(?P<slug>[\w\-]+)/$', LegaltextView.as_view(), name='legaltext'),
]

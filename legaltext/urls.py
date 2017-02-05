from django.conf.urls import url

from .views import LegaltextView

urlpatterns = [
    url(r'^(?P<slug>.*)$', LegaltextView.as_view(), name='legaltext'),
]

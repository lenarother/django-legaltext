from django.conf.urls import include, url
from django.contrib import admin

from .views import LegaltextView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<slug>.*)/$', LegaltextView.as_view(), name='legaltext'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^(?P<string>[a-zA-Z0-9]+)/$', views.urlRedirect, name='redirect'),

]

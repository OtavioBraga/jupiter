# -*- coding: utf-8 -*-
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r'^$', view=views.UserServicesView.as_view(), name='home'),
    # url(regex=r'^$', view=views.HomeView.as_view(), name='publisher-home'),
    url(regex=r'^service/new/$', view=views.NewServiceView.as_view(),
        name='new-service')
]

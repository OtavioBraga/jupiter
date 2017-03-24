# -*- coding: utf-8 -*-
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from .forms import MyAuthenticationForm 


urlpatterns = [
    url(r'^login/$', 
        auth_views.login,
         {'template_name': 'login.html', 'authentication_form':MyAuthenticationForm},
          name='login'),

    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
]

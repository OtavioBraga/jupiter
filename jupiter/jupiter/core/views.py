from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, TemplateView
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from .models import Service, UserService

from .forms import NewServiceForm

class UserObjectsMixin(object):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class NewServiceView(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    form_class = NewServiceForm
    initial = {'key': 'value'}
    template_name = 'service/new_service.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NewServiceView, self).form_valid(form)


class UserServicesView(LoginRequiredMixin, UserObjectsMixin, ListView):
    login_url = '/user/login/'
    template_name = "service/list_services.html"
    context_object_name = 'services'
    model = UserService

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('turn_off'):
            id = int(self.request.POST.get('turn_off'))
            service = UserService.objects.get(id=id)
            service.kill()
        if self.request.POST.get('turn_on'):
            id = int(self.request.POST.get('turn_on'))
            service = UserService.objects.get(id=id)
            service.start()
        if self.request.POST.get('delete'):
            id = int(self.request.POST.get('delete'))
            service = UserService.objects.get(id=id)
            service.delete()
        return HttpResponseRedirect('/')
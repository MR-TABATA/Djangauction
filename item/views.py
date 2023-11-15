from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, ListView
from .models import Item
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeIndexView(LoginRequiredMixin, ListView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'DjangAuction Item List'
    return context
  queryset = Item.objects.filter(deleted__isnull=True,).all()
  template_name = 'item/index.html'


# Create your views here.

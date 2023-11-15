from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, ListView
from item.models import Item, Stat, Watch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncDate
from django.db.models import Sum, Count



# Create your views here.

class HomeIndexView(LoginRequiredMixin, ListView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['title'] = 'DjangAuction Dashboard'

    context['histories'] = (
      Stat.objects.select_related().filter(deleted__isnull=True, custom_user=self.request.user.pk).
      annotate(date=TruncDate('item__close')).values('date').
      annotate(sum=Sum('win_price'), count=Count('win_price')).values('sum', 'count', 'date').
      order_by('-date')
    )

    return render(request, 'dashboard/index.html', context)


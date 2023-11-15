from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, ListView
from item.models import Item, Stat, Watch, Maker, Bid, BidHistory, Rule
from fee.models import Fee, UserFee
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncDate
from django.db.models import Sum, Count
from config.consts import PHOTO_FILE_PATH
from .libraries import first_price_auction, second_price_auction
import os

import datetime
from django.utils.timezone import make_aware
from django.utils import timezone

from django.db.models import Q
import unicodedata
from functools import reduce
from operator import and_

from auction.forms import BidForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from config.libraries import maker_count, calculated_bidding, calculated_commiting

from django.http import JsonResponse
from django.urls import reverse_lazy, reverse

# Create your views here.

class HomeIndexView(LoginRequiredMixin, ListView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['title'] = 'DjangAuction Auction'

    condition = Q()
    condition_featured_1 = Q(item__featured__gte=1)
    condition_featured_0 = Q(item__featured=0)

    if 'maker_id' in request.GET and len(request.GET['maker_id']) != 0 :
      condition = Q(item__maker__id = request.GET['maker_id']) & Q(item__deleted__isnull=True) & Q(item__close__gte=datetime.datetime.now())
      context['selected_maker'] = Maker.objects.values('id', 'maker_name').annotate(count=Count('id')).filter(deleted__isnull=True, id = request.GET['maker_id']).first()
    else:
      condition = Q(item__deleted__isnull=True) &  Q(item__close__gte=datetime.datetime.now())

    context['featured'] = (Stat.objects.select_related('item', 'item__maker').filter(condition & condition_featured_1).order_by('-item__featured', 'item__sort'))
    context['items'] = (Stat.objects.select_related('item', 'item__maker').filter(condition & condition_featured_0).order_by('-item__featured', 'item__sort'))

    context['maker_count'] = maker_count(datetime.datetime.now())


    return render(request, 'auction/index.html', context)

class DetailView(LoginRequiredMixin, FormView):
  model=Bid
  form_class=BidForm
  template_name = 'auction/detail.html'

  def get_success_url(self):
    return reverse('auction:detail', kwargs = {'pk': self.kwargs['pk']})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'DjangAuction Auction'
    context['crumbs'] = [
      ['Auction Top', 'auction:index'],
      ['Auction Detail', ''],
    ]
    #watch
    context['is_watch'] = Watch.objects.filter(item_id=self.kwargs['pk'], custom_user_id=self.request.user.pk).first()

    # アクセス数
    stat_data = Stat.objects.filter(item_id=self.kwargs['pk'], deleted__isnull=True).first()
    stat_object = Stat.objects.get(pk=stat_data.pk)
    stat_object.access_count = stat_object.access_count + 1
    stat_object.save()

    stat = Stat.objects.select_related('item', 'item__maker').filter(item__id=self.kwargs['pk']).first()
    alphabets = [chr(i) for i in range(97, 97 + 26)]
    tmp_alphabet = []
    for alphabet in alphabets:
      if os.path.isfile(PHOTO_FILE_PATH + '/' + stat.item.code + alphabet + '.jpg'):
        tmp_alphabet.append(alphabet)
    context['thumsbnail_alphas'] = tmp_alphabet
    context['item'] = stat
    context['bid'] = Bid.objects.filter(item__id=self.kwargs['pk'], deleted__isnull=True, custom_user=self.request.user.pk).order_by('-id').first()
    context['bid_histories'] = BidHistory.objects.filter(item=self.kwargs['pk']).order_by('-history_price', '-created')

    #watch登録
    if not context['is_watch']:
      watched_object = Watch(item_id=self.kwargs['pk'], custom_user_id=self.request.user.pk)
      watched_object.save()

    return context

  def post(self, request, *args, **kwargs):
    form = self.get_form(self.form_class)

    if form.is_valid():
      if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return self.ajax_response(form)
      # Ajax 以外のPOSTメソッドの処理
      return super().form_valid(form)
    else:
      # フォームデータが正しくない場合の処理
      return super().form_invalid(form)

  def ajax_response(self, form):
    #return first_price_auction(self, form)
    return second_price_auction(self, form)


class WatchView(LoginRequiredMixin, ListView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['title'] = 'DjangAuction Auction'

    sql = (" SELECT da_stat.*, da_item.code, da_item.item_name, "
           " da_watch.item_id, da_maker.maker_name "
           " FROM da_item, da_stat, da_watch, da_maker "
           " WHERE da_item.id = da_stat.item_id "
           " AND da_item.id = da_watch.item_id "
           " AND da_item.maker_id = da_maker.id "
           " AND da_item.deleted IS Null "
           " AND da_watch.deleted IS Null "
           " AND da_stat.deleted IS Null "
           " AND da_watch.custom_user_id = %s "
           " ORDER BY da_watch.id DESC")
    context['watches'] = Item.objects.raw(sql, [self.request.user.pk,])

    return render(request, 'auction/watch.html', context)

class HistoryView(LoginRequiredMixin, ListView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['title'] = 'DjangAuction Auction'

    context['histories'] = (
      Stat.objects.select_related().filter(deleted__isnull=True, custom_user=self.request.user.pk).
      annotate(date=TruncDate('item__close')).values('date').
      annotate(sum=Sum('win_price'), count=Count('win_price')).values('sum', 'count', 'date').
      order_by('-date')[:10]
    )

    return render(request, 'auction/histories.html', context)


class TransactionPaginator(Paginator):
  def validate_number(self, number):
    try:
      return super().validate_number(number)
    except EmptyPage:
      if int(number) > 1:
          # return the last page
          return self.num_pages
      elif int(number) < 1:
          # return the first page
          return 1
      else:
          raise

class TransactionView(LoginRequiredMixin, ListView):
  paginator_class = TransactionPaginator
  paginate_by = 100

  def get(self, request, *args, **kwargs):
    context = {}
    page = self.request.GET.get('page', 1)
    context['title'] = 'DjangAuction Auction'

    condition = Q(item__deleted__isnull=True) & Q(win_price__gt=0)

    if 'item_name' in request.GET and len(request.GET['item_name']) != 0:
      keywords = request.GET['item_name'].replace('　', ' ').strip(' ').split()
      condition_keyword = reduce(and_,[Q(item__item_name__icontains=q) for q in keywords])
      condition = condition & condition_keyword
      context['item_name'] = request.GET['item_name']

    if 'maker_id' in request.GET and len(request.GET['maker_id']) != 0 :
      condition = condition & Q(item__maker__id = request.GET['maker_id'])
      context['selected_maker'] = Maker.objects.values('id', 'maker_name').annotate(count=Count('id')).filter(deleted__isnull=True, id = request.GET['maker_id']).first()

    items = Stat.objects.select_related('item', 'item__maker').filter(condition).order_by('-item__close')
    paginator = self.paginator_class(items, self.paginate_by)
    items = paginator.page(page)
    context['items'] = paginator.page(page)

    context['maker_count'] = maker_count('2000-01-01')

    return render(request, 'auction/transactions.html', context)


class RuleView(ListView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['title'] = 'DjangAuction Auction'

    context['rules'] = Rule.objects.filter(deleted__isnull=True)

    return render(request, 'auction/rules.html', context)

class MyDealView(LoginRequiredMixin, ListView):
  def get(self, request, *args, **kwargs):
    context = {}
    context['title'] = 'DjangAuction Auction'
    context['close'] = self.kwargs['close']

    sql = ( " SELECT max(da_bid.bid_price) AS max, da_stat.win_price, da_stat.custom_user_id,"
            " da_item.id, da_item.item_name, da_item.maker_id, da_item.close, da_maker.maker_name"
            " FROM da_item, da_bid, da_stat, da_maker"
            " WHERE da_bid.item_id = da_item.id"
            " AND da_item.id = da_stat.item_id"
            " AND da_item.id = da_bid.item_id"
            " AND da_item.maker_id = da_maker.id"
            " AND da_bid.custom_user_id = %s"
            " AND DATE_FORMAT(da_item.close, '%%Y-%%m-%%d') = %s"
            " GROUP BY da_stat.win_price, da_stat.custom_user_id, da_item.id, da_item.item_name,"
            " da_item.maker_id, da_item.close"
            " ORDER BY da_item.maker_id")
    context['items'] = Item.objects.raw(sql, [self.request.user.pk, self.kwargs['close']])

    sql = ( " SELECT da_stat.win_price, da_item.id, da_item.item_name,"
            " da_item.maker_id, da_item.start_price, da_item.close,"
            " da_maker.maker_name, da_stat.bid_count, da_stat.access_count"
            " FROM accounts_customuser, da_item, da_stat, da_maker"
            " WHERE da_item.custom_user_id = accounts_customuser.id"
            " AND accounts_customuser.id = %s "
            " AND DATE_FORMAT(da_item.close, '%%Y-%%m-%%d') = %s "
            " AND da_stat.item_id = da_item.id"
            " AND da_maker.id = da_item.maker_id"
            " ORDER BY da_stat.win_price desc" )
    context['commits'] = Item.objects.raw(sql, [self.request.user.pk, self.kwargs['close']])

    bidding = calculated_bidding(self.request.user.pk, self.kwargs['close'])

    context['bidding_win_sum'] = bidding['sum_win_price']
    context['bidding_fee'] = bidding['bidding_fee']
    context['bidding_unit_fee'] = bidding['bidding_unit_fee']
    context['bidding_win_count'] = bidding['bidding_win_count']
    context['summaries'] = bidding['summaries']
    context['bidding_total'] = bidding['sum_win_price']+bidding['bidding_fee']

    commits = calculated_commiting(self.request.user.pk, self.kwargs['close'])

    if commits['summary']['sum_win_price']:
      context['commision_fee'] = commits['commision_fee']
      context['commision_count'] = commits['commision_count']
      context['commit_summary'] = commits['summary']
      context['fee'] = commits['fee']
      context['commit_total'] = commits['summary']['sum_win_price']-commits['commision_fee']

    return render(request, 'auction/my_deal.html', context)
from django.urls import path
from .views import (
  HomeIndexView, WatchView, HistoryView, DetailView,
  TransactionView, RuleView, MyDealView
)
from . import views

app_name = 'auction'

urlpatterns=[
  path('', HomeIndexView.as_view(), name='index'),
  path('detail/<int:pk>', DetailView.as_view(), name='detail'),
  path('watch/', WatchView.as_view(), name='watch'),
  path('transaction/', TransactionView.as_view(), name='transaction'),
  path('rule/', RuleView.as_view(), name='rule'),
  path('my_deal/<str:close>', MyDealView.as_view(), name='my_deal'),
]




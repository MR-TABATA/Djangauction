from django.urls import path
from .views import HomeIndexView
from . import views

app_name = 'dashboard'

urlpatterns=[
  path('', HomeIndexView.as_view(), name='index'),
]




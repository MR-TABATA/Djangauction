from django.urls import path
from .views import (
  MainFileResponseView, EstimateFileResponseView, ThumsnailFileResponseView, IndexView,
  SuperUserFileResponseView
)
from . import views
from django.views.generic.base import RedirectView

app_name = 'config'

urlpatterns=[
  path('main/<str:code>', MainFileResponseView.as_view(), name='main_file_view'),
  path('estimate/<str:code>', EstimateFileResponseView.as_view(), name='estimate_file_view'),
  path('thumsbnail/<str:code>/<str:alpha>', ThumsnailFileResponseView.as_view(), name='thumsbnail_file_view'),
  path('file/<str:file_name>', SuperUserFileResponseView.as_view(), name='file_view'),
  path('', IndexView.as_view(), name='index')
]




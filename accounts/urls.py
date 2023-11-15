from django.urls import path
from accounts.views import Signin, Signout, PasswordModify, PasswordModifiedView, ProfileDetail, UserUpdate
from . import views

app_name = 'accounts'

urlpatterns=[
  path('signin/', Signin.as_view(), name='signin'),
  path('signout/', Signout.as_view(),name='signout'),
  path('password_modify/', PasswordModify.as_view(), name='password_modify'),
  path('password_modified/', PasswordModifiedView.as_view(), name='password_modified'),
  path('profile/', ProfileDetail.as_view(), name='profile_detail'),
  path('profile/<int:pk>/edit', UserUpdate.as_view(), name='profile_edit'),
  path('media/', views.MediaView.as_view(), name='media'),
]




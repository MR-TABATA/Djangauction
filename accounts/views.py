from django.shortcuts import render, resolve_url
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from .forms import UsernameAuthenticationForm, PasswordModifyForm
from django.views.generic import FormView, DetailView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm
from core.settings import base
from PIL import Image
import io
from django.http import HttpResponse

CustomUser = get_user_model()


class Signin(LoginView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Start Django Auction Signin'
    return context
  form_class = UsernameAuthenticationForm
  template_name = 'accounts/signin.html'


class Signout(LogoutView):
  template_name = 'accounts/signout.html'


class PasswordModify(PasswordChangeView):
  """パスワード変更ビュー"""
  form_class = PasswordModifyForm
  success_url = reverse_lazy('accounts:password_modified')
  template_name = 'accounts/password_modify.html'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['notifications'] = getNotifications()
    return context


class PasswordModifiedView(PasswordChangeDoneView):
  template_name = 'accounts/password_modified.html'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['notifications'] = getNotifications()
    return context


class ProfileDetail(LoginRequiredMixin, TemplateView):
  model = CustomUser
  template_name = 'accounts/profile.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['notifications'] = getNotifications()
    return context

class UserUpdate(LoginRequiredMixin, UpdateView):
  model = CustomUser
  form_class = ProfileUpdateForm
  template_name = 'accounts/profile_edit.html'
  success_url = reverse_lazy('accounts:profile_detail')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['notifications'] = getNotifications()
    return context


class MediaView(LoginRequiredMixin, View):
  """ 画像取得 のビュー """
  def get(self, request, *args, **kwargs):
    img_path = CustomUser.objects.filter(deleted__isnull=True, id=self.request.user.pk).first()
    img = Image.open(base.MEDIA_ROOT+'/'+str(img_path.avater))
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=img.format)
    imgByteArr = imgByteArr.getvalue()

    response = HttpResponse(imgByteArr, status=200)
    response["Content-Type"] = "image/jpeg"
    response["Content-Disposition"] = "inline; filename={0}".format(img)
    return response

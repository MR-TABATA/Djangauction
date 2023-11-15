from django.http import FileResponse
from django.views.generic.base import View
from .consts import PHOTO_FILE_PATH, APPLY_FILE_PATH
from django.contrib.auth.mixins import LoginRequiredMixin
from management.mixins import SuperuserRequiredMixin
from django.shortcuts import render, redirect
import os


class IndexView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    if self.request.user.is_superuser:
      return redirect('management:index')
    else :
      return redirect('auction:index')


class MainFileResponseView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    if os.path.isfile(PHOTO_FILE_PATH + '/' + self.kwargs['code'] + '.jpg'):
      response = FileResponse(open(PHOTO_FILE_PATH + '/' + self.kwargs['code'] + '.jpg', 'rb'))
    else:
      response = FileResponse(open(PHOTO_FILE_PATH + '/dummy_450x300.jpg', 'rb'))

    return response


class EstimateFileResponseView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    if os.path.isfile(PHOTO_FILE_PATH + '/g' + self.kwargs['code'] + '.jpg'):
      response = FileResponse(open(PHOTO_FILE_PATH + '/g' + self.kwargs['code'] + '.jpg', 'rb'))
    else:
      response = FileResponse(open(PHOTO_FILE_PATH + '/dummy_450x300.jpg', 'rb'))

    return response


class ThumsnailFileResponseView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    if os.path.isfile(PHOTO_FILE_PATH+'/'+self.kwargs['code']+self.kwargs['alpha']+'.jpg'):
      response = FileResponse(open(PHOTO_FILE_PATH+'/'+self.kwargs['code']+self.kwargs['alpha']+'.jpg', 'rb'))

    return response


class SuperUserFileResponseView(SuperuserRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    if os.path.isfile(APPLY_FILE_PATH + '/' + self.kwargs['file_name']):
      response = FileResponse(open(APPLY_FILE_PATH + '/' + self.kwargs['file_name'], 'rb'))
    else:
      response = FileResponse(open(PHOTO_FILE_PATH + '/dummy_450x300.jpg', 'rb'))

    return response
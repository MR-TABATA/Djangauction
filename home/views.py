from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, ListView
from inquiry.forms import InquiryModelForm
from home.forms import ApplyModelForm
from inquiry.models import Inquiry
from fee.models import Fee
from home.models import Apply, Mail
from django.contrib import messages
from config.libraries import sendmailByBrevo
from anymail.message import AnymailMessage

class HomeIndexView(FormView, ListView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Star AuctionHub'
    return context
  queryset = Fee.objects.filter(deleted__isnull=True, top_display='show')
  form_class = InquiryModelForm
  template_name = 'home/index.html'
  success_url = '/'

  def form_valid(self, form):
    messages.success(self.request, "お問い合わせを受付ました")
    Inquiry.objects.create(
      name=form.cleaned_data['name'],
      mail=form.cleaned_data['mail'],
      subject=form.cleaned_data['subject'],
      contents=form.cleaned_data['contents']
    )

    return super().form_valid(form)


class ApplyFormView(FormView) :
  form_class = ApplyModelForm
  template_name = 'home/apply.html'
  success_url = '/'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'AuctionHub 加入申込'
    context["fee"] = Fee.objects.filter(deleted__isnull=True, id=self.kwargs['pk']).first()
    return context

  def form_valid(self, form):
    messages.success(self.request, "加入申し込みを受付ました")
    applied = Apply.objects.filter(deleted__isnull=True, license_number=form.cleaned_data['license_number']).first()
    if not applied:
      Apply.objects.create(
        fee=Fee.objects.get(id=self.kwargs['pk']),
        license_number = form.cleaned_data['license_number'],
        representative_name = form.cleaned_data['representative_name'],
        company_name = form.cleaned_data['company_name'],
        zip = form.cleaned_data['zip'],
        prefecture = form.cleaned_data['prefecture'],
        address = form.cleaned_data['address'],
        block = form.cleaned_data['block'],
        building = form.cleaned_data['building'],
        phone = form.cleaned_data['phone'],
        mobile_phone = form.cleaned_data['mobile_phone'],
        email = form.cleaned_data['email'],
      )

      option = Mail.objects.filter(deleted__isnull=True, subject='加入申し込み受領').first()
      message = sendmailByBrevo(option.subject, option.body, form.cleaned_data['email'], option.bcc)
      message.send()

    return super().form_valid(form)

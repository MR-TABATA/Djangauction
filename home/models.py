from django.db import models
from config.models import BaseModel
from fee.models import Fee
# Create your models here.

class Apply(BaseModel):
  fee = models.ForeignKey(Fee, verbose_name='年会費及び手数料', on_delete=models.SET_NULL, blank=True, null=True, related_name='apply_fee')
  license_number = models.CharField(verbose_name='古物許可証番号', max_length=100, blank=True, null=True)
  representative_name = models.CharField(verbose_name='代表者', max_length=100, blank=True, null=True)
  company_name = models.CharField(verbose_name='会社名または屋号', max_length=100, blank=True, null=True)
  zip = models.CharField(verbose_name='郵便番号', max_length=10, blank=True, null=True)
  prefecture = models.CharField(verbose_name='都道府県', max_length=10, blank=True, null=True)
  address = models.CharField(verbose_name='市区町村', max_length=100, blank=True, null=True)
  block = models.CharField(verbose_name='番地', max_length=100, blank=True, null=True)
  building = models.CharField(verbose_name='建物等', max_length=100, blank=True, null=True)
  phone = models.CharField(verbose_name='連絡先', max_length=15, blank=True, null=True)
  mobile_phone = models.CharField(verbose_name='モバイル', max_length=15, blank=True, null=True)
  email = models.EmailField(verbose_name='メール', max_length=200, blank=True, null=True)

  def __str__(self):
    return self.company_name

  class Meta:
    db_table = 'da_apply'
    verbose_name = '加入申し込み'
    verbose_name_plural = '加入申し込み'

class Mail(BaseModel):
  subject = models.CharField(verbose_name='メールタイトル', max_length=100, blank=True, null=True)
  body = models.TextField(verbose_name='メール本文', max_length=5000, blank=True, null=True)
  to = models.CharField(verbose_name='宛先', max_length=100, blank=True, null=True)
  bcc = models.CharField(verbose_name='BCC', max_length=100, blank=True, null=True)

  def __str__(self):
    return self.subject

  class Meta:
    db_table = 'da_mail'
    verbose_name = 'メールオプション情報'
    verbose_name_plural = 'メールオプション情報'
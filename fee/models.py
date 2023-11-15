from django.db import models
from config.models import BaseModel
from accounts.models import CustomUser

# Create your models here.
class Fee(BaseModel):
  section = models.CharField(verbose_name='名称', max_length=100, blank=True, null=True)
  subscriptionByYear = models.IntegerField(verbose_name='年会費', blank=True, null=True)
  systemUsageByYear = models.IntegerField(verbose_name='システム利用料/回', blank=True, null=True)
  commission = models.IntegerField(verbose_name='成約手数料', blank=True, null=True)
  commission_margin = models.DecimalField(verbose_name='成約手数料マージン', max_digits=5, decimal_places=3, blank=True, null=True)
  bidding = models.IntegerField(verbose_name='落札手数料', blank=True, null=True)
  bidding_margin = models.DecimalField(verbose_name='落札手数料マージン', max_digits=5, decimal_places=3, blank=True, null=True)
  started = models.DateTimeField(verbose_name='適用日開始', blank=True, null=True)
  ended = models.DateTimeField(verbose_name='適用日終了', blank=True, null=True)
  top_display = models.CharField(verbose_name='トップ画面表示対象', max_length=20, blank=True, null=True, default='show')
  featured = models.CharField(verbose_name='お勧めプラン', max_length=20, blank=True, null=True, default='on')
  custom_user = models.ManyToManyField(CustomUser, through="UserFee")

  def __str__(self):
    return self.section

  class Meta:
    db_table = 'da_fee'
    verbose_name = '年会費及び手数料'
    verbose_name_plural = '年会費及び手数料'


class UserFee(BaseModel):
  custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_fee_user')
  fee         = models.ForeignKey(Fee, on_delete=models.SET_NULL, blank=True, null=True, related_name='fee')

  def __str__(self):
    return self.custom_user.company_name

  class Meta:
    db_table = 'da_user_fee'
    verbose_name = '会員年会費・手数料'
    verbose_name_plural = '会員年会費・手数料'


class Offset(BaseModel):
  custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='offset_user')
  fee = models.ForeignKey(Fee, on_delete=models.SET_NULL, blank=True, null=True, related_name='offset_fee')
  bidded_sum = models.IntegerField(verbose_name='落札合計金額', blank=True, null=True)
  commissioned_sum = models.IntegerField(verbose_name='成約合計金額', blank=True, null=True)
  commission_count = models.IntegerField(verbose_name='成約点数', blank=True, null=True)
  commission_fee_sum = models.IntegerField(verbose_name='成約料', blank=True, null=True)
  bidding_count = models.IntegerField(verbose_name='落札点数', blank=True, null=True)
  bidding_fee_sum = models.IntegerField(verbose_name='落札料', blank=True, null=True)
  counterbalance = models.IntegerField(verbose_name='相殺金額', blank=True, null=True)
  close = models.DateTimeField(verbose_name='終了日時', blank=True, null=True)


  def __str__(self):
    return self.custom_user.company_name

  class Meta:
    db_table = 'da_offset'
    verbose_name = 'オークション相殺表'
    verbose_name_plural = 'オークション相殺表'

class Tax(BaseModel):
  tax_rate = models.DecimalField(verbose_name='消費税率', max_digits=5, decimal_places=3, blank=True, null=True)
  started = models.DateTimeField(verbose_name='適用日開始', blank=True, null=True)
  ended = models.DateTimeField(verbose_name='適用日終了', blank=True, null=True)

  def __str__(self):
    return self.tax_rate

  class Meta:
    db_table = 'da_tax'
    verbose_name = '消費税率'
    verbose_name_plural = '消費税率'
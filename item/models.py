from django.db import models
from config.models import BaseModel
from accounts.models import CustomUser


class Maker(BaseModel):
  id = models.CharField(verbose_name='メーカーID', max_length=5, primary_key=True)
  maker_name = models.CharField(verbose_name='メーカー名', max_length=100, blank=True, null=True)
  sort = models.IntegerField(verbose_name='並び',blank=True, null=True)

  def __str__(self):
    return self.maker_name

  class Meta:
    db_table = 'da_maker'
    verbose_name = 'メーカー'
    verbose_name_plural = 'メーカー'


# Create your models here.
class Item(BaseModel):
  custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='item_user')
  maker = models.ForeignKey(Maker, verbose_name='メーカー', on_delete=models.SET_DEFAULT, default='1', blank=True, null=True, related_name='item_maker')
  code = models.CharField(verbose_name='当社番号', max_length=10, blank=True, null=True)
  type = models.CharField(verbose_name='種類', max_length=50, blank=True, null=True)
  featured = models.IntegerField(verbose_name='お勧め', blank=True, null=True)
  item_name = models.CharField(verbose_name='品名', max_length=100, blank=True, null=True)
  description = models.TextField(verbose_name='商品説明', max_length=1000, blank=True, null=True)
  serial = models.CharField(verbose_name='製造番号', max_length=100, blank=True, null=True)
  sort = models.IntegerField(verbose_name='並び',blank=True, null=True)
  close = models.DateTimeField(verbose_name='終了日時', blank=True, null=True)
  start_price = models.IntegerField(verbose_name='スタート金額', blank=True, null=True)

  def __str__(self):
    return self.item_name

  class Meta:
    db_table = 'da_item'
    verbose_name = 'アイテム'
    verbose_name_plural = 'アイテム'


class Stat(BaseModel):
  custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default='1', blank=True, null=True, related_name='winner_user')
  item = models.ForeignKey(Item, on_delete=models.SET_NULL, default='1', blank=True, null=True, related_name='winner_item')
  win_price = models.IntegerField(verbose_name='落札金額',blank=False, null=False, default='0')
  bid_count = models.IntegerField(verbose_name='入札回数',blank=False, null=False, default='0')
  access_count = models.IntegerField(verbose_name='アクセス数',blank=False, null=False, default='0')

  def __str__(self):
    return self.item.item_name

  class Meta:
    db_table = 'da_stat'
    verbose_name = 'スタッツ'
    verbose_name_plural = 'スタッツ'


class Bid(BaseModel):
  custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='bid_user')
  item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True, related_name='bid_item')
  bid_price = models.IntegerField(verbose_name='入札金額',blank=True, null=True)

  def __str__(self):
    return self.item.item_name

  class Meta:
    db_table = 'da_bid'
    verbose_name = '入札'
    verbose_name_plural = '入札'

class BidHistory(BaseModel):
  custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='bid_history_user')
  item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True, related_name='bid_history_item')
  history_price = models.IntegerField(verbose_name='入札金額',blank=True, null=True)

  def __str__(self):
    return self.item.item_name

  class Meta:
    db_table = 'da_bid_history'
    verbose_name = '入札履歴'
    verbose_name_plural = '入札履歴'


class Watch(BaseModel):
  custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='watch_user')
  item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True, related_name='watch_item')

  def __str__(self):
    return self.custom_user.company_name

  class Meta:
    db_table = 'da_watch'
    verbose_name = 'お気に入り'
    verbose_name_plural = 'お気に入り'


class Rule(BaseModel):
  chapter = models.CharField(verbose_name='章', max_length=20, blank=True, null=True)
  article = models.CharField(verbose_name='条', max_length=50, blank=True, null=True)
  body = models.TextField(verbose_name='本文', max_length=1000, blank=True, null=True)
  option = models.CharField(verbose_name='附則', max_length=1000, blank=True, null=True)

  def __str__(self):
    return f"{self.article}"

  class Meta:
    db_table = 'da_rule'
    verbose_name = '規約'
    verbose_name_plural = '規約'
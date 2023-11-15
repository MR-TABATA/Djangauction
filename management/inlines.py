from django.contrib import admin
from fee.models import UserFee
from item.models import Bid, BidHistory



class UserFeeInline(admin.TabularInline):
  model = UserFee
  fields = ['fee', 'get_fee_section', 'get_fee_subscriptionByYear', 'get_fee_started', 'get_fee_ended']
  readonly_fields = ['get_fee_section', 'get_fee_subscriptionByYear', 'get_fee_started', 'get_fee_ended','created', 'modified', 'deleted']

  def get_fee_section(self, obj):
    return obj.fee.section

  def get_fee_subscriptionByYear(self, obj):
    return '¥'+str(f"{obj.fee.subscriptionByYear:,}")

  def get_fee_started(self, obj):
    return obj.fee.started

  def get_fee_ended(self, obj):
    return obj.fee.ended

  get_fee_section.short_description='会費・手数料コース'
  get_fee_subscriptionByYear.short_description='年会費'
  get_fee_started.short_description='コース適用開始日'
  get_fee_ended.short_description='コース適用終了日'

  can_delete = False
  max_num = 0
  extra = 0
  show_change_link = True


class BidInline(admin.TabularInline):
  model = Bid
  fields = ['get_bidder', 'bid_price', 'format_created', ]
  readonly_fields = ['get_bidder', 'bid_price', 'format_created', 'modified', 'deleted']
  ordering = ('-bid_price', 'id',)

  def get_bidder(self, obj):
    return obj.custom_user.company_name

  def format_created(self, obj):
    return obj.created.strftime('%Y-%m-%d %H:%M:%S.%f')

  format_created.short_description = '入札日時マイクロ秒'

  can_delete = False
  max_num = 0
  extra = 0
  show_change_link = True

class BidHistoryInline(admin.TabularInline):
  model = BidHistory
  fields = ['get_bidder', 'history_price', 'format_created', ]
  readonly_fields = ['get_bidder', 'history_price', 'format_created', 'modified', 'deleted']
  ordering = ('-id',)

  def get_bidder(self, obj):
    return obj.custom_user.company_name

  def format_created(self, obj):
    return obj.created.strftime('%Y-%m-%d %H:%M:%S.%f')

  format_created.short_description = '入札日時マイクロ秒'

  can_delete = False
  max_num = 0
  extra = 0
  show_change_link = True
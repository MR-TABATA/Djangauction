from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import TextInput, Textarea
from django.db import models

import os
from config.consts import PHOTO_FILE_PATH

from config.models import BaseModel
from accounts.models import CustomUser
from item.models import Maker, Item, Stat, Bid, BidHistory, Watch, Rule
from fee.models import Fee, UserFee, Offset
from inquiry.models import Inquiry
from home.models import Apply, Mail
from management.inlines import UserFeeInline, BidInline, BidHistoryInline

from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from management.resource import (
  MyUserResource,
)

from django.contrib.auth.hashers import make_password
import re
from django.utils.safestring import mark_safe
from django.utils import timezone
import datetime
from django.db.models import Q

from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.http import HttpResponse, JsonResponse
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

# Register your models here.

class MyUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = '__all__'



class MyUserCreationForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ('company_name', 'representative_name', 'username',)


class MyUserAdmin(ImportExportModelAdmin, UserAdmin):
  fieldsets = (
    (_('名前等'), {'fields': ( 'company_name', 'representative_name', 'username',)}),
    (_('プロフィール'), {'fields': ('zip', 'prefecture', 'address', 'block', 'building', 'phone', 'mobile_phone', 'email')}),
    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'password')}),
    (_('生成・更新・削除'), {'fields': ('created', 'modified', 'deleted')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'password1', 'password2'),
    }),
  )

  form = MyUserChangeForm
  add_form = MyUserCreationForm
  inlines = [UserFeeInline]

  list_display = ('company_name', 'representative_name', 'username', 'email', 'is_staff')
  list_filter = ('is_staff', 'is_superuser', 'is_active')
  search_fields = ('company_name', 'representative_name', 'email', 'username')
  readonly_fields = ['created', 'modified', 'deleted']

  ordering = ('id',)
  resource_class = MyUserResource

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()


class ItemAdmin(ExtraButtonsMixin, ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('id', 'maker', 'featured', 'item_name', 'show_thumsbnail_images', 'serial',  'sort', )
  list_display_links = ('item_name',)
  list_editable = ('sort',)
  ordering = ('-id', '-featured', 'sort',)
  fieldsets = (
    (None, {'fields': ('code', 'maker', 'item_name', 'featured', 'description', 'serial', 'close', 'sort', 'start_price',  'show_images',)}),
  )
  search_fields = ['item_name']
  list_filter = ['close', 'maker']

  inlines = [BidHistoryInline, BidInline]

  formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '40'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
  }

  def get_readonly_fields(self, request, obj=None):
    if obj and obj.close:
      return ['code', 'maker', 'item_name', 'featured', 'serial', 'sort', 'start_price', 'show_images', 'created', 'modified', 'deleted']
    return ['show_images', 'created', 'modified', 'deleted']

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.select_related('maker').all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def show_thumsbnail_images(self, obj):
    alphabets = [chr(i) for i in range(97, 97 + 26)]
    thumsbnail = []
    to_return=''
    for alphabet in alphabets:
      if os.path.isfile(PHOTO_FILE_PATH + '/' + obj.code + alphabet + '.jpg'):
        (thumsbnail.
         append('<img src="/config/thumsbnail/{}" style="width:100px;height:auto;border:1px solid #000000;">'.format(obj.code + '/' + alphabet))
        )
        to_return = mark_safe(' '.join(thumsbnail))

    return to_return

  def show_images(self, obj):
    alphabets = [chr(i) for i in range(97, 97 + 26)]
    thumsbnail = []
    to_return=''
    for alphabet in alphabets:
      if os.path.isfile(PHOTO_FILE_PATH + '/' + obj.code + alphabet + '.jpg'):
        (thumsbnail.
         append('<img src="/config/thumsbnail/{}" style="width:360px;height:auto;border:1px solid #000000;">'.format(obj.code + '/' + alphabet))
        )
        to_return = mark_safe(' '.join(thumsbnail))
    return to_return

  show_thumsbnail_images.short_description = 'サムネイル画像'
  show_images.short_description = 'アイテム画像'

  @link(href=None,
        change_list=True,
        change_form=False,
        html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
  def image_upload(self, button):
    button.label = f"アイテム画像アップロード"
    button.href = f"/management/upload_image/"




class FeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('section', 'featured', 'subscriptionByYear', 'systemUsageByYear', 'started','ended', 'modified',)
  readonly_fields = ['created', 'modified', 'deleted']
  ordering = ('id',)

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()


class UserFeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('get_company_name', 'fee',)
  list_display_links = ('get_company_name',)
  readonly_fields = ['created', 'modified', 'deleted']
  ordering = ('id',)

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.select_related('fee', 'custom_user').filter(deleted__isnull=True)

  def get_company_name(self, obj):
    return obj.custom_user.company_name

  get_company_name.short_description = '会社名'



class OffsetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  fieldsets = (
    (None,
     {'fields':
       (
         'custom_user_company_name', 'close', 'counterbalance', 'fee_section', 'bidded_sum', 'commissioned_sum', 'display_count', 'display_fee_sum',
         'commission_count', 'commission_fee_sum', 'bidding_count', 'bidding_fee_sum',
       )
     }
     ),
  )

  list_display = ('custom_user_company_name', 'close', 'counterbalance')
  readonly_fields = [
    'custom_user_company_name', 'fee_section', 'close', 'created', 'modified', 'deleted'
  ]
  list_display_links = ['custom_user_company_name']
  #ordering = ('id',)

  def custom_user_company_name(self, obj):
    return obj.custom_user.company_name

  def fee_section(self, obj):
    return obj.fee.section

  custom_user_company_name.short_description = '会社名'
  fee_section.short_description = 'コース名称'

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all().order_by('-id')

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()



class MailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  fieldsets = (
    (None,
      {'fields':('subject', 'bcc', 'to', 'body',)}
    ),
  )

  list_display = ('subject', 'bcc', )
  readonly_fields = ['created', 'modified', 'deleted']
  ordering = ('id',)

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

class ApplyAdmin(admin.ModelAdmin):
  fieldsets = (
    (None,
      {'fields':('company_name', 'representative_name', 'license_number', 'zip', 'prefecture','address', 'block', 'building', 'phone', 'mobile_phone', 'email')}
    ),
  )

  list_display = ('company_name', 'representative_name', 'license_number', 'fee_section', 'modified',)
  readonly_fields = ['company_name', 'representative_name', 'license_number', 'zip', 'prefecture','address', 'block', 'building', 'phone', 'mobile_phone', 'email', 'created', 'modified', 'deleted']
  ordering = ('id',)

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def fee_section(self, obj):
    return obj.fee.section
  fee_section.short_description = '種類'

  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

class InquiryAdmin(admin.ModelAdmin):
  fieldsets = (
    (None,
      {'fields':('name', 'mail', 'subject', 'contents')}
    ),
  )

  list_display = ('name', 'mail', 'subject', 'modified',)
  readonly_fields = ['name', 'mail', 'subject', 'contents', 'created', 'modified', 'deleted']
  ordering = ('id',)

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

class WatchAdmin(admin.ModelAdmin):
  list_display = ('custom_user_company_name', 'item_item_name', 'modified',)
  fieldsets = (
    (None,
     {'fields':
       (
         'custom_user_company_name', 'item_item_name', 'modified',
       )
     }
     ),
  )

  def custom_user_company_name(self, obj):
    return obj.custom_user.company_name
  def item_item_name(self, obj):
    return obj.item.item_name
  custom_user_company_name.short_description = '会社名'
  item_item_name.short_description = 'アイテム名'

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

class StatAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  list_display = ('item_item_name', 'win_price', 'custom_user_company_name', 'item_close', 'format_created',)
  fieldsets = (
    (None,
     {'fields':
       (
         'item_item_name', 'win_price', 'custom_user_company_name', 'bid_count', 'access_count', 'format_created',
       )
     }
     ),
  )
  readonly_fields = [
    'custom_user_company_name', 'item_item_name', 'win_price', 'bid_count', 'access_count', 'item_close',
    'modified', 'created', 'modified', 'deleted'
  ]


  def custom_user_company_name(self, obj):
    return obj.custom_user.company_name
  def item_item_name(self, obj):
    return obj.item.item_name
  def format_created(self, obj):
    return obj.created.strftime('%Y-%m-%d %H:%M:%S.%f')

  def item_close(self, obj):
    return obj.item.close

  format_created.short_description = '入札日時マイクロ秒'
  custom_user_company_name.short_description = '落札社'
  item_item_name.short_description = 'アイテム名'
  item_close.short_description = '終了日時'

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.select_related('item').filter(Q(deleted__isnull=True)).all().order_by('-item__close')

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

class MakerAdmin(admin.ModelAdmin):
  fieldsets = (
    (None,
      {'fields':('id', 'maker_name', 'sort', )}
    ),
  )

  list_display = ('id', 'maker_name', 'sort', 'modified',)
  readonly_fields = ['created', 'modified', 'deleted']
  ordering = ('sort',)
  list_editable = ('sort',)

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

class BidAdmin(admin.ModelAdmin):
  list_display = ('custom_user_company_name', 'item_item_name', 'bid_price', 'modified',)
  fieldsets = (
    (None,
     {'fields':
       (
         'custom_user_company_name', 'item_item_name', 'bid_price', 'modified',
       )
     }
     ),
  )
  readonly_fields = ['custom_user_company_name', 'item_item_name', 'bid_price', 'modified', 'created', 'modified', 'deleted']
  def custom_user_company_name(self, obj):
    return obj.custom_user.company_name
  def item_item_name(self, obj):
    return obj.item.item_name
  custom_user_company_name.short_description = '会社名'
  item_item_name.short_description = 'アイテム名'

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

class BidHistoryAdmin(admin.ModelAdmin):
  list_display = ('custom_user_company_name', 'item_item_name', 'history_price', 'modified',)
  fieldsets = (
    (None,
     {'fields':
       (
         'custom_user_company_name', 'item_item_name', 'history_price', 'modified',
       )
     }
     ),
  )
  readonly_fields = ['custom_user_company_name', 'item_item_name', 'history_price', 'modified', 'created', 'modified', 'deleted']
  def custom_user_company_name(self, obj):
    return obj.custom_user.company_name
  def item_item_name(self, obj):
    return obj.item.item_name
  custom_user_company_name.short_description = '会社名'
  item_item_name.short_description = 'アイテム名'

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()

  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

class RuleAdmin(admin.ModelAdmin):
  list_display = ('chapter', 'article', 'body',)
  fieldsets = (
    (None,
     {'fields':
       (
         'chapter', 'article', 'option', 'body', 'modified',
       )
     }
     ),
  )
  readonly_fields = ['created', 'modified', 'deleted']
  list_display_links = ('body',)
  ordering = ('id',)

  def delete_model(self, request, obj):
    obj.deleted = timezone.now()
    obj.save()

  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.filter(deleted__isnull=True).all()

  def delete_queryset(self, request, queryset):
    for obj in queryset:
      obj.deleted = timezone.now()
      obj.save()


admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Maker, MakerAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Stat, StatAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(BidHistory, BidHistoryAdmin)
admin.site.register(Watch, WatchAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(UserFee, UserFeeAdmin)
admin.site.register(Offset, OffsetAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(Mail, MailAdmin)
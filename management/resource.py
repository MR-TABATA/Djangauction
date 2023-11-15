from config.models import BaseModel
from accounts.models import CustomUser
from item.models import Maker, Item, Stat, Bid, BidHistory, Watch, Rule
from fee.models import Fee
from inquiry.models import Inquiry
from home.models import Apply

from import_export.resources import ModelResource
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.formats import base_formats
from import_export.widgets import Widget

from django.contrib.auth.hashers import make_password
import re
from django.utils.safestring import mark_safe
from django.utils import timezone


class MyUserResource(ModelResource):
  def before_import_row(self, row, **kwargs):
    value = row['password']
    #空白、または20文字以上の場合、ハッシュ化する
    if len(row['password']) < 20 & len(row['password']) > 0:
      row['password'] = make_password(value)
  class Meta:
    model = CustomUser
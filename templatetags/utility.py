# templatetags/cut_re.py
import re
import datetime
import calendar
from django import template

register = template.Library()

@register.filter
def cut_re(value, search): 
    return re.sub(search, "", value)


@register.filter
def split(value, key):
    return value.split(key)

@register.filter(name="multiple")
def multiple(value, args):
    """掛け算"""
    return '{:.0f}'.format(value * args)

@register.filter(name="multiplePlus")
def multiplePlus(value, args):
    """帳票用掛け算"""
    return value * args

@register.filter(name="multiplePlusOne")
def multiplePlusOne(value, args):
    """掛け算"""
    return value * args+1

@register.filter(name='datetime_to_unix')
def datetime_to_unix(value):
    return int(datetime.datetime.timestamp(value))

@register.filter(name='get_last_date')
def get_last_date(value):
    return value.replace(day=calendar.monthrange(value.year, value.month)[1])

@register.filter(name='replace_comma')
def replace_comma(value):
    return str(value).replace(',', '')

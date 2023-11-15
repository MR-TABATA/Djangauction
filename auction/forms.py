from django import forms
from django.utils.translation import gettext_lazy as _
from item.models import Stat
from django.core.exceptions import ValidationError

def verify_digit(value):
  if value > 999999:
    raise ValidationError('100万円以下でお願いします')

class BidForm(forms.Form):
  bid_price = forms.IntegerField(
    label=_(""),
    widget=forms.TextInput(attrs={'autofocus': True, 'placeholder':'あいうえお'}),
    required=True,
    #validators=[verify_digit]
  )
  bid_count = forms.HiddenInput()
  access_count = forms.HiddenInput()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'


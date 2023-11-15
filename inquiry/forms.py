from django import forms
from django.forms import ModelForm, Textarea
from .models import Inquiry

class InquiryModelForm(forms.ModelForm):
  class Meta:
    model = Inquiry
    exclude = ['deleted',]
    widgets = {
      "contents": Textarea(attrs={ "rows": 10}),
    }

  def __init__(self, *args, **kwargs):
    for field in self.base_fields.values():
      field.widget.attrs["class"] = "form-control"
    super().__init__(*args, **kwargs)
    self.label_suffix = ""
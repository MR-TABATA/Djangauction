from django import forms
from django.forms import ModelForm, Textarea
from .models import Apply

class ApplyModelForm(forms.ModelForm):
  class Meta:
    model = Apply
    exclude = ['deleted', 'fee']

  def __init__(self, *args, **kwargs):
    for field in self.base_fields.values():
      field.widget.attrs["class"] = "form-control"
    super().__init__(*args, **kwargs)
    self.label_suffix = ""

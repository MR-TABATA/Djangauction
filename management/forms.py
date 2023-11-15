from django import forms
from django.forms import formset_factory
from item.models import Item
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

def check_length(value):
    if len(value) < 10:
        raise ValidationError('Title length is short.')

class ItemForm(forms.ModelForm):
    code = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    type = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    featured = forms.IntegerField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    item_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    serial = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    estimate = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    custom_user = forms.IntegerField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    description = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    maker = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )
    start_price = forms.IntegerField(label=False, widget=forms.TextInput(attrs={'class': 'form-control'}), )

    class Meta:
        model = Item
        fields = [
            "code", "type", "featured", "item_name", "serial", "estimate", "custom_user", "description", "maker", "start_price",
        ]

EditItemFormSet = forms.modelformset_factory(Item, form=ItemForm, extra=0)
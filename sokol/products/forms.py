from django import forms
from .models import Product


class GetCharacteristics(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('price', 'product_sleng', 'meter',)

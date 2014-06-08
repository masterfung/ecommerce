from django import forms

from .models import Product


class ProductQtyForm(forms.ModelForm):
    quantity = forms.IntegerField()
    class Meta:
        model = Product
        fields = ['slug']
    

from django import forms

from products.models import Product

class ProductQtyForm(forms.ModelForm):
    quantity = forms.IntegerField()
    class Meta:
        model = Product
        fields = ['slug']
    

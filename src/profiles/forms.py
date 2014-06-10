from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
	"""docstring for AddressForm"""
	class Meta:
		model = Address
		fields = ( 'address1', 'address2', 'city', 'state', 'postal_code', 'country')
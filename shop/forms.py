from django import forms
from shop.models import Customer, Phone
from django import forms
from shop.models import Customer,Transaction,Phone

class CustomerForm(forms.Form):
    name = forms.CharField(max_length=30, label="Customer Name")
    discount = forms.IntegerField(label="Discount (%)", min_value=0, max_value=100)

class PhoneForm(forms.Form):
    item = forms.CharField(label='Phone Name', max_length=200)
    price = forms.FloatField(label='Price')

class TransactionForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), label='Customer')
    phone = forms.ModelChoiceField(queryset=Phone.objects.all(), label='Phone')
    qty = forms.IntegerField(min_value=1, label='Quantity')

from django import forms
from apps.shipping.models import Address
from apps.orders.models import Payment

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method']


class ComprobanteForm(forms.Form):
    method = forms.ChoiceField(choices=[
        ('NEQUI', 'Nequi'),
        ('DAVIPLATA', 'Daviplata'),
        ('BANK', 'Transferencia Bancaria'),
    ])
    comprobante = forms.ImageField()
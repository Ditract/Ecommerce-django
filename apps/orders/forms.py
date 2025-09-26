from django import forms
from apps.shipping.models import Address
from apps.orders.models import Payment


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        labels = {
            "full_name": "Nombre completo",
            "street": "Calle",
            "city": "Ciudad",
            "province": "Departamento/Provincia",
            "country": "País",
            "postal_code": "Código Postal",
            "phone": "Teléfono",
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method']
        labels = {
            "method": "Método de pago",
        }


class ComprobanteForm(forms.Form):
    method = forms.ChoiceField(
        label="Método de pago",
        choices=[
            ('NEQUI', 'Nequi'),
            ('DAVIPLATA', 'Daviplata'),
            ('BANK', 'Transferencia Bancaria'),
        ]
    )
    comprobante = forms.ImageField(label="Subir comprobante")

from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_city', 'delivery_phone', 'payment_method', 'special_instructions']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 2}),
            'special_instructions': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['delivery_address'].initial = user.address
            self.fields['delivery_phone'].initial = user.phone
            self.fields['delivery_city'].initial = ''
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')

from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address',
                  'postal_code', 'city', 'delivery_container']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_container'].widget.attrs.update({'class': 'form-select'})

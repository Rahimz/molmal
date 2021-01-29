from django import forms

# the min and max quantity user could buy
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)  # convert input to integer

    # override indicates whether the quantity should update or not
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)  # we do not like to show it to the user

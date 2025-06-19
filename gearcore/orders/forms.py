from django import forms

class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    delivery_address = forms.CharField(required=False)

    requires_delivery = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ("0", False),
            ("1", True)
        ],
        initial="0"
    )

    payment_on_get = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ("0", False),
            ("1", True)
        ],
        initial="0"
    )


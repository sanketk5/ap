from django import forms

PAYMENT_CHOICES = (
    ('COD', 'Cash on delievery '),
    ('onlinePay', 'onlinePay')
)


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your address',
        'class': 'form-control'
    }), required=True)
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your city',
        'class': 'form-control'
    }), required=False)
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Maharashtra',
        'class': 'form-control'
    }), required=False)
    pin_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Pin code',
        'class': 'form-control',
    }), required=True)
    contact_no = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter contact no.',
        'class': 'form-control'
    }), required=True)
    refer_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter reference code.',
        'class': 'form-control'
    }), required=False)
    save_info = forms.BooleanField(
        widget=forms.widgets.CheckboxInput(), required=False)


class PaymentForm(forms.Form):
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    payment_sender_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Please enter sender name.',
        'class': 'form-control'
    }), required=False)


class RefundForm(forms.Form):
    # order_id = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()

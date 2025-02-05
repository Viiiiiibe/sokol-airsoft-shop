from django import forms
from .models import Order, DeliveryOrder
from phonenumber_field.formfields import PhoneNumberField


class MakingAnOrderForm(forms.ModelForm):
    customer_last_name = forms.CharField
    customer_first_name = forms.CharField
    customer_patronymic = forms.CharField
    customer_email = forms.EmailField
    customer_phone = PhoneNumberField
    customer_vk = forms.CharField
    customer_telegram = forms.CharField

    class Meta:
        model = Order
        # fields = "__all__"
        fields = ('customer_last_name', 'customer_first_name', 'customer_patronymic', 'customer_email',
                  'customer_phone', 'customer_vk', 'customer_telegram', 'customer_comment',)


class MakingAnDeliveryOrderForm(forms.ModelForm):
    customer_last_name = forms.CharField
    customer_first_name = forms.CharField
    customer_patronymic = forms.CharField
    customer_email = forms.EmailField
    customer_phone = PhoneNumberField
    customer_vk = forms.CharField
    customer_telegram = forms.CharField

    class Meta:
        model = DeliveryOrder
        # fields = "__all__"
        fields = ('customer_last_name', 'customer_first_name', 'customer_patronymic', 'customer_email',
                  'customer_phone', 'customer_vk', 'customer_telegram', 'customer_comment',)

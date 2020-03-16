from django import forms
from .models import Subscriber


class SubscriberCreateForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['first_name', 'last_name', 'phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Subscriber.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already subscribed for updates")
        return phone_number

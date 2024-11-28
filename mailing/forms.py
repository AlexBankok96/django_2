from django import forms

from .models import Mailing, Message, Recipient


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"
        widgets = {
            "recipients": forms.CheckboxSelectMultiple(),
        }


class RecipientForm(forms.ModelForm):

    class Meta:


        model = Recipient

        fields = "__all__"


class MessageForm(forms.ModelForm):

    class Meta:

        model = Message
        fields = "__all__"
__author__ = 'eyob'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Yaas.models import Auction, AuctionCategory

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit = False)
            user.email = self.cleaned_data['email']

            if commit:
                user.save()
            return user

#Form for Auction
class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction

#Form for category
class AuctionCategoryForm(forms.ModelForm):

    class Meta:
        model = AuctionCategory
__author__ = 'eyob'

from django import forms
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm
from Yaas.models import Auction, AuctionCategory, Bidder

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']

            if commit:
                user.save()
            return user

#Form for Auction
class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ('auction_name', 'auction_description','price_min','category','end_date')

        def clean_end_date(self):
            cd = self.cleaned_data

            end_date = cd.get('end_date')
            if(end_date-datetime.now())<timedelta(hours=72):
                raise forms.ValidationError('End date should be at least 72 hours from now')
            return end_date

#Form for category
class AuctionCategoryForm(forms.ModelForm):

    class Meta:
        model = AuctionCategory

class BidAuctionForm(forms.ModelForm):

    class Meta:
        model = Bidder


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
        except User.DoesNotExist:
            pass

    email = forms.EmailField(label="Primary Email")

    class Meta:
        model = User

    def save(self,*args, **kwargs):
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(EditProfileForm, self).save(*args, **kwargs)
        return profile

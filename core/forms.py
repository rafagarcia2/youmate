from django import forms

from core.models import Profile


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class UpdateProfileAboutForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about',)

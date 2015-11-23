from django import forms

from core.models import Profile
from interest.models import Interest


class ProfileInterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple(), required=True)

    class Meta:
        model = Profile
        fields = ()

    def clean_interests(self):
        interests_clean = self.cleaned_data['interests']
        if len(interests_clean) > 3:
            raise forms.ValidationError(
                "You can't choose more than three items!")
        return interests_clean
